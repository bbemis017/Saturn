from django.shortcuts import render, HttpResponseRedirect
from website.models import Website


def testTemplate(request):
    return render(request,"website/resumeTemplate.html",locals())

def test(request,domain):
    website = Website.objects.get(domain=domain)
    return HttpResponseRedirect(website.path)
