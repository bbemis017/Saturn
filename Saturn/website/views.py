from django.shortcuts import render


def testTemplate(request):
    return render(request,"website/resumeTemplate.html",locals())
