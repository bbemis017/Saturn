from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, authenticate
from ratelimit.decorators import ratelimit
from django.forms.utils import ErrorList
from accounts.models import Accounts
from accounts.forms import (
    SignupForm,
    SigninForm,
    ForgetForm,
    EditUserProfileForm,
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

    if not _is_bad_verification(email, verification_code):
        user.account.verified = True
        verification_success = True
    else:
        invalid_verification_code = True

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
@ratelimit(key='post:email', rate='5/m', block=True)
def send_verification_email(request):
    email_sent = False
    if request.is_ajax:
        user.account.generate_verification_code()
        user.account.save()
        user.save()
        EmailService.send_activate_email(user)
    return JsonResponse({
        'email_sent': email_sent
    })


@ratelimit(key='post:email', rate='5/m', block=True)
def signup(request):
    if request.method != "POST":
        signup_form = SignupForm()
        return render(request, "accounts/signup.html", locals())

    signup_form = SignupForm(request.POST)

    if signup_form.is_valid():
        first_name = signup_form.cleaned_data['first_name'];
        last_name = signup_form.cleaned_data['last_name'];
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
        #update values in the account for first_name and last_name
        user.account.save()


        try:
            EmailService.send_activate_email(user)
            email_sent = True
        except:
            email_sent = False

        user = authenticate(username=username, password=password)
        django_login(request, user)
        next = request.GET.get('next', '')
        if next == '':
            next = '/'
        return HttpResponseRedirect(next) 

    return render(request, "accounts/signup.html", locals())

def signin(request):
    if request.method != "POST":
        signin_form = SigninForm()
        return render(request, "accounts/login.html", locals())

    signin_form = SigninForm(request.POST)

    if signin_form.is_valid():
        username = signin_form.cleaned_data['username_or_email']
        password = signin_form.cleaned_data['password']
        key = 'email__iexact' if '@' in username else 'username__iexact'
        if User.objects.filter(**{key: username}).exists():
            user = User.objects.get(**{key: username})
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                next = request.GET.get('next', '')
                if next == '':
                    next = '/accounts/profile'
                return HttpResponseRedirect(next)
            else:
                error = signin_form._errors.setdefault("Unable to log in!", ErrorList())
                return render(request, "accounts/login.html", locals())
    else:
        login_err = True
        return render(request, "accounts/login.html",locals())

def reset_password(request):
    #Set true if user needs to enter confirmation code
    enterconfirmation = False
    #Set true if user needs to enter new password
    enterpassword = False

    return render(request, 'accounts/reset_password.html',locals())

@login_required
def profile(request):
    if request.user.is_authenticated():
        #the user has logged in
        account = Accounts.objects.get(user=request.user)

        print account
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

            print "account"
            editProfile_form = EditUserProfileForm(request.POST)
            print editProfile_form.errors
            
            if editProfile_form.is_valid():
                #save information 
                account.first_name = editProfile_form.cleaned_data['first_name']
                account.last_name = editProfile_form.cleaned_data['last_name']
                account.save()
                print("valid")
                update_success = True
                return render(request, "accounts/dashboard.html",locals())

        return render(request, "accounts/dashboard.html", locals())    
    # the user hasn't logged in yet
    return render(request, "accounts/login.html", locals())


def dashboard(request):
    return render(request, "accounts/dashboard.html", locals())

def sites(request):
    return render(request, "accounts/sites.html", locals())
