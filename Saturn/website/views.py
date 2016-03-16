from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from website.models import Website
from website.models import Template, ResumeTemplate
from website.forms import CreateSiteForm,CreateTemplateForm,CreateResumeTemplateForm, DeleteSiteForm
from accounts.models import Accounts
from section.models import Section, Post
from section.constants import SectionTypes



def displaySite(request,domain):
    website = Website.objects.get(domain=domain)

    #slightly more convenient variables
    template = website.template
    if template.path == "website/resumeTemplate.html":
        template = template.resumetemplate

    sections = Section.objects.filter(template=template)

    return render(request,template.path,locals())
     
@login_required
def createSite(request):
    #for information displayed on navigation bar
    account = Accounts.objects.get(user=request.user)

    if request.method == "POST":

       #if client requests to check domain availability
       if 'domain_json' in request.POST:
           domain_json = request.POST.get('domain_json')
           response_data = {}
           if Website.objects.filter(domain=domain_json).exists():
               response_data['exists'] = 1
           else:
               response_data['exists'] = 0
           return JsonResponse(response_data)
       
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
