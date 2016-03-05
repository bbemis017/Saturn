from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from website.models import Website
from website.forms import CreateSiteForm
from accounts.models import Accounts


def testTemplate(request):
    return render(request,"website/resumeTemplate.html",locals())

def test(request,domain):
    website = Website.objects.get(domain=domain)
    return render(request,"website/resumeTemplate.html",locals())
    #not necessary
    #return HttpResponseRedirect(website.path)

@login_required
def createSite(request):
    #for information displayed on navigation bar
    account = Accounts.objects.get(user=request.user)

    if request.method == "POST":

       createSiteForm = CreateSiteForm(request.POST)
       if createSiteForm.is_valid():

           domain = createSiteForm.cleaned_data['domain']

           #check if site exists
           if not Website.objects.filter(domain=domain).exists():
               #create Site
               website = Website.objects.create(user=request.user)
               website.domain = domain
               website.save()
               return HttpResponseRedirect("/accounts/sites")
           else:
               #error
               errorDomainExists = True
               return render(request,"website/createSite.html",locals())

    return render(request, "website/createSite.html",locals())
