from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from website.models import Website
from website.models import Template
from website.forms import CreateSiteForm,CreateTemplateForm
from accounts.models import Accounts


def testTemplate(request):
    return render(request,"website/resumeTemplate.html",locals())

def displaySite(request,domain):
    website = Website.objects.get(domain=domain)
    template = website.template
    return render(request,"website/resumeTemplate.html",locals())
     
@login_required
def createSite(request):
    #for information displayed on navigation bar
    account = Accounts.objects.get(user=request.user)

    if request.method == "POST":

       createSiteForm = CreateSiteForm(request.POST)
       createTemplateForm = CreateTemplateForm(request.POST)
       if createSiteForm.is_valid() and createTemplateForm.is_valid():
           domain = createSiteForm.cleaned_data['domain']
           title = createTemplateForm.cleaned_data['title']
           
           #check if site exists
           if not Website.objects.filter(domain=domain).exists():
               template = Template.objects.create(title=title,path="website/resumeTemplate.html")
               template.save()
               #create Site
               website = Website.objects.create(user=request.user,template=template)
               website.domain = domain
               website.template = template
               website.save()
               return HttpResponseRedirect("/accounts/sites")
           else:
               #error
               errorDomainExists = True
               return render(request,"website/createSite.html",locals())

    return render(request, "website/createSite.html",locals())
