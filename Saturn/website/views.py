from django.shortcuts import render
from website.models import Website


def testTemplate(request):
    return render(request,"website/resumeTemplate.html",locals())
