from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, authenticate
from ratelimit.decorators import ratelimit
from accounts.forms import (
    SignupForm,
    SigninForm,
    ForgetForm,
)
from utils.email import EmailService


@ratelimit(key='post:email', rate='5/m', block=True)
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
            errors = signup_form._errors.setdefault("username", ErrorList())
            errors.append(u"Already Exists")
            return render(request, "accounts/signup.html", locals())
        
        user = signup_form.save(commit=False)
        user.set_password(password)
        user.save()

        EmailService.send_activate_email(user)
        user = authenticate(username=username, password=password)
        django_login(request, user)
        next = request.GET.get('next', '')
        return HttpResponseRedirect(next) 

    return render(request, "accounts/signup.html", locals())
