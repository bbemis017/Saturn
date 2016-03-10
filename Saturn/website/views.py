from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from website.models import Website
from website.models import Template, ResumeTemplate
from website.forms import CreateSiteForm,CreateTemplateForm,CreateResumeTemplateForm
from accounts.models import Accounts


def displaySite(request,domain):
    website = Website.objects.get(domain=domain)

    #slightly more convenient variables
    template = website.template
    if template.path == "website/resumeTemplate.html":
        template = template.resumetemplate

    return render(request,template.path,locals())
     
@login_required
def createSite(request):
    #for information displayed on navigation bar
    account = Accounts.objects.get(user=request.user)

    if request.method == "POST":

       createSiteForm = CreateSiteForm(request.POST)
       createTemplateForm = CreateTemplateForm(request.POST)
       createResumeTemplateForm = CreateResumeTemplateForm(request.POST)

       if createSiteForm.is_valid() and createTemplateForm.is_valid() and createResumeTemplateForm.is_valid():
           domain = createSiteForm.cleaned_data['domain']
           title = createTemplateForm.cleaned_data['title']
           author = createResumeTemplateForm.cleaned_data['author']
           description = createResumeTemplateForm.cleaned_data['description']
           
           #check if site exists
           if not Website.objects.filter(domain=domain).exists():
               # creates a resume template by default
               template = ResumeTemplate.objects.create(title=title,description=description)
               template.path = "website/resumeTemplate.html"
               template.author = author
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
