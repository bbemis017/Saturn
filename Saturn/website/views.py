from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
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

    sections = list(Section.objects.filter(template=template))

    #change type of section to subclass
    for section in sections:
        if section.childType == SectionTypes.POST:
            temp = section.unique_name
            sections.append(Post.objects.get(unique_name=section.unique_name))
            sections.remove(section)
        elif section.childType == SectionTypes.DEFAULT:
            print "default"
        else:
            #undefined child type
            print "error in displaySite"
            print "undefined Section Type: " + section.childType


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
