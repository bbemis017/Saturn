from django.shortcuts import render

# Create your views here.

def testTemplate(request):
    return render(request,"website/resumeTemplate.html",locals())
