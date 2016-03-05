from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, authenticate
from ratelimit.decorators import ratelimit
from django.forms.utils import ErrorList
from accounts.models import Accounts
from website.models import Website
from accounts.forms import (
    SignupForm,
    SigninForm,
    EditUserProfileForm,
    ResetPasswordForm,
)
from utils.email import EmailService


@ratelimit(key='get:email', rate='5/m', block=True)
def activate(request):
    if not ('verification_code' in request.GET and 'email' in request.GET):
        return HttpResponseRedirect('/accounts/signup/')

    email = request.GET['email']
    verification_code = request.GET['verification_code']

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
    else:
        return HttpResponseRedirect('/accounts/signup/')

    if _is_bad_verification(email, verification_code):
        invalid_verification_code = True
    else:
        user.account.verified = True
        verification_success = True

    return render(request, "accounts/profile.html", locals())


def _is_bad_verification(email, verification_code):
    if not User.objects.filter(email=email).exists():
        return True
    user = User.objects.get(email=email)
    
    if user.account.verification_code != verification_code or \
            user.account.expire_at is not None and user.account.expire_at < timezone.now():
        return True
    else:
        return False


@login_required
@ratelimit(key='post:email', rate='5/m', block=True, method=['POST'])
def send_verification_email(request):
    email_sent = False
    if request.is_ajax:
        user = request.user
        user.account.generate_verification_code()
        user.account.save()
        user.save()
        EmailService.send_activate_email(user)
    return JsonResponse({
        'email_sent': email_sent
    })


@ratelimit(key='post:email', rate='5/m', block=True, method=['POST'])
def signup(request):
    if request.method != "POST":
        signup_form = SignupForm()
        return render(request, "accounts/signup.html", locals())

    signup_form = SignupForm(request.POST)

    if signup_form.is_valid():
        email = signup_form.cleaned_data['email']
        username = signup_form.cleaned_data['username']
        password = signup_form.cleaned_data['password']
        if User.objects.filter(email__iexact=email).exists():
            errors = signup_form._errors.setdefault("email", ErrorList())
            errors.append(u"Already Exists")
            return render(request, "accounts/signup.html", locals())
        
        user = signup_form.save(commit=False)
        user.set_password(password)
        user.save()
        user.account.generate_verification_code()
        user.account.save()


        try:
            EmailService.send_activate_email(user)
            email_sent = True
        except:
            email_sent_fail = False

        user = authenticate(username=username, password=password)
        django_login(request, user)
        next = request.GET.get('next', '')
        if next == '':
            next = '/accounts/profile/'
        return HttpResponseRedirect(next) 

    return render(request, "accounts/signup.html", locals())


@ratelimit(key='post:username', rate='5/m', block=True, method=['POST'])
def signin(request):
    if request.method != "POST":
        signin_form = SigninForm()
        return render(request, "accounts/login.html", locals())

    signin_form = SigninForm(request.POST)

    if not signin_form.is_valid():
        login_err = True
        return render(request, "accounts/login.html",locals())
        
    username = signin_form.cleaned_data['username']
    password = signin_form.cleaned_data['password']
    key = 'email__iexact' if '@' in username else 'username__iexact'
    if User.objects.filter(**{key: username}).exists():
        user = User.objects.get(**{key: username})
        user = authenticate(username=username, password=password)
        if user is None:
            login_err = True
            return render(request, "accounts/login.html", locals())
    else:
        login_err = True
        return render(request, "accounts/login.html", locals())

    django_login(request, user)
    next = request.GET.get('next', '')
    if next == '':
        next = '/accounts/profile/'
    return HttpResponseRedirect(next)


@ratelimit(key='post:email', rate='10/m', block=True, method=['POST'])
def reset_password(request):
    if 'email' not in request.GET and 'email' not in request.POST:
        reset_missing_email = True
        return render(request, "accounts/reset_password.html", locals())

    if 'email' in request.POST and 'verification_code' not in request.GET:
        email_sent = True
        email = request.POST.get('email')
        try:
            user = User.objects.get(email__iexact=email)
            user.account.generate_verification_code()
            user.account.save()
            EmailService.send_verification_email(user)
        except:
            email_not_exist = True
        return render(request, "accounts/reset_password.html", locals())

    if 'verification_code' not in request.GET:
        verification_code_error = True
        return render(request, "accounts/reset_password.html", locals())

    email = request.GET.get('email')
    verification_code = request.GET.get('verification_code')

    forgot_form = ResetPasswordForm(request.POST)

    if _is_bad_verification(email, verification_code):
        bad_verification = True
        return render(request, "accounts/reset_password.html", locals())

    if request.method != 'POST':
        return render(request, "accounts/reset_password.html", locals())

    if not forgot_form.is_valid():
        return render(request, "accounts/reset_password.html", locals())

    if forgot_form.cleaned_data['password'] != forgot_form.cleaned_data['confirm_password']:
        confirm_password_error = True
        return render(request, "accounts/reset_password.html", locals())

    user = User.objects.get(email=forgot_form.cleaned_data['email'])
    user.set_password(forgot_form.cleaned_data['password'])
    user.save()

    account = user.account
    account.verification_code = "%s" % timezone.now()
    account.expire_at = timezone.now()
    account.save()

    user = authenticate(username=user.username, password=forgot_form.cleaned_data['password'])
    django_login(request, user)

    next = request.GET.get('next', '')
    if next == '':
        next = '/accounts/profile/'
    return HttpResponseRedirect(next)

@login_required
def profile(request):
    account = Accounts.objects.get(user=request.user)

    editInfo = False 
    if request.method != "POST":
        #editProfile_form = EditUserProfileForm(instance=account)
        return render(request, "accounts/dashboard.html", locals())

    if 'edit' in request.POST:
        #user has clicked on edit
        editInfo = True
    elif 'submit' in request.POST:
        #user has clicked on submit
        editInfo = False

        editProfile_form = EditUserProfileForm(request.POST)
        
        if editProfile_form.is_valid():
            account.first_name = editProfile_form.cleaned_data['first_name']
            account.last_name = editProfile_form.cleaned_data['last_name']
            account.save()
            update_success = True
            return render(request, "accounts/dashboard.html",locals())

    return render(request, "accounts/dashboard.html", locals())    


@login_required
def sites(request):

    account = Accounts.objects.get(user=request.user)
    websites = Website.objects.filter(user=request.user)

    if request.method == "POST":

        #create Site
        if 'createSite' in request.POST:
            return HttpResponseRedirect("/sites/createSite")

    #otherwise render site page
    return render(request, "accounts/sites.html", locals())
