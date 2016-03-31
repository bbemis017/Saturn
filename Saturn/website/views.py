from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from website.models import Website
from website.models import Template, ResumeTemplate
from website.forms import CreateSiteForm,CreateTemplateForm,CreateResumeTemplateForm, DeleteSiteForm
from accounts.models import Accounts
from section.models import Section, Post, Experience
from section.constants import SectionTypes

import json



def displaySite(request,domain):
    website = Website.objects.get(domain=domain)

    #slightly more convenient variables
    template = website.template
    if template.path == "website/resumeTemplate.html":
        template = template.resumetemplate

    sections = Section.objects.filter(template=template, user=website.user)

    return render(request,template.path,locals())

@login_required
def createSite(request):
    #for information displayed on navigation bar
    account = Accounts.objects.get(user=request.user)

    if request.method == "POST":

        if request.is_ajax():

            response_data = {}

            if 'submit' in request.POST:
                domain = request.POST.get('domain')
                title = request.POST.get('title')
                author = request.POST.get('author')
                description = request.POST.get('description')

                if 'skills' in request.POST:
                    skills = json.loads( request.POST.get('skills') )
                if 'majors' in request.POST:
                    majors = json.loads(request.POST.get('majors'))
                if 'languages' in request.POST:
                    languages = json.loads(request.POST.get('languages'))
                if 'experience' in request.POST:
                    print request.POST
                    experience = "no experience" #json.loads(request.POST.get('experience'))
                if 'name' in request.POST:
                    name = "no name" #json.loads(request.POST.get('name')) #this should be changed to something that is more clear

                '''there are variables for every field on the createSite page 
                that are being sent through the ajax. Most variables can be 
                accessed the way above but some variables contain a list and 
                you must call json.loads to convert them into an array I left an
                example of skills above. Sections are slightly different. It is
                still an array but the even elements contain the section title
                and the odd elements contain the section content, so there are
                2 elements per section.If you are confused about that please ask.
                List of variables:
                  -Array variables:
                     skills, languages, sections, majors
                  -Normal variables:
                    domain, title, author, description, name, education, gpa,
                    experience
                '''

               #check if site exists
                if not Website.objects.filter(domain=domain).exists():
                    # creates a resume template by default
                    template = ResumeTemplate.objects.create(title=title,description=description)
                    template.path = "website/resumeTemplate.html" # i am ignoring the template selection since we have only 1 template
                    template.author = author
                    template.save()

                    experience = Experience.objects.create(user=request.user,template=template)
                    experience.skills = skills
                    experience.company_name = name
                    experience.languages = languages
                    experience.save()

                    #create Site
                    website = Website.objects.create(user=request.user,template=template)
                    website.domain = domain
                    website.template = template
                    website.save()
                    
                    response_data = {}
                    response_data['redirect'] = "/accounts/sites";
                    '''also keep in mind that if an ajax function calls this
                    python function then we must return a json file. In this case
                    I have the javascript pickup the redirect, and redirect the
                    browser'''
                    return JsonResponse(response_data);
                else:
                    #error
                    errorDomainExists = True
                    response_data['error'] = 1
                    return JsonResponse(response_data);

            #if client requests to check domain availability
            if 'domain_check' in request.POST:
                domain_json = request.POST.get('domain_json')
                if Website.objects.filter(domain=domain_json).exists():
                    response_data['exists'] = 1
                else:
                    response_data['exists'] = 0
                return JsonResponse(response_data)

    return render(request, "website/createSite.html",locals())
