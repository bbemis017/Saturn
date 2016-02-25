from django.shortcuts import render
from django.template import Template, Context
from django.template.loader import get_template
from django.http import HttpResponse


def home(request):
	return render(request, "home.html", locals())

def reset_password(request):
        #Set true if user need to enter new password
        enterpassword = False
        #Set true if user need to enter confirmation code
        enterconfirmation = False

        context = Context({'enterpassword':enterpassword, 'enterconfirmation':enterconfirmation})
        return render(request, 'reset_password.html', context)
