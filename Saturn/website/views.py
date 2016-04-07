from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from website.models import Website
from website.models import Template, ResumeTemplate
from website.forms import CreateSiteForm,CreateTemplateForm,CreateResumeTemplateForm, CreateCourseWebpageTemplateForm, DeleteSiteForm
from accounts.models import Accounts
from section.models import Introduction, Summary, Section, Post, Experience
from section.constants import SectionTypes

import json



def displaySite(request,domain):
    website = Website.objects.get(domain=domain)

    #slightly more convenient variables
    template = website.template
    if template.path == "website/resumeTemplate.html":
        template = template.resumetemplate
    elif template.path == "website/courseTemplate.hrml":
        template = template.coursetemplate

    sections = Section.objects.filter(template=template, user=website.user)

    return render(request,template.path,locals())

def varExists(request,string):
    if string in request.POST and request.POST.get(string) != '':
        return True
    else:
        return False
def arrayExists(request,string):
    variable = ''
    try:
        variable = json.loads( request.POST.get(string) )
    except ValueError, e:
        return False
    if len(variable) == 1 and variable[0] == '':
        return False 
    elif len(variable):
        return True
    else:
        return False

@login_required
def createSite(request):
    #for information displayed on navigation bar
    account = Accounts.objects.get(user=request.user)

    if request.method == "POST":

        #determine the type of form to display
        if 'resumeTemplate' in request.POST:
            resumeTemplate = True
        elif 'courseTemplate' in request.POST:
            courseTemplate = True

        elif request.is_ajax():

            response_data = {}

            if 'submit' in request.POST:

                print request.POST

                #check essentials
                if not varExists(request,'domain'):
                    response_data['domain_missing'] = 1
                    response_data['error'] = 1
                if not varExists(request,'title'):
                    response_data['title_missing'] = 1
                    response_data['error'] = 1
                if 'error' in response_data:
                    return JsonResponse(response_data)
                 
                domain = request.POST.get('domain')
                title = request.POST.get('title')
                author = request.POST.get('author')
                description = request.POST.get('description')

                sections = {} 

                #check and assign variables
                if arrayExists(request,'sections'):
                    sections = json.loads(request.POST.get('sections') )
                if varExists(request,'summary'):
                    summary = request.POST.get('summary')

                #check if site exists
                if not Website.objects.filter(domain=domain).exists():
<<<<<<< HEAD
=======
                    # creates a resume template by default
                    template = ResumeTemplate.objects.create(title=title)
                    template.path = "website/resumeTemplate.html"
                    template.author = author
                    template.save()

                    if varExists(request,'summary'):
                        summ = Post.objects.create(user=request.user,template=template)
                        summ.title = "About Me"
                        summ.content = summary
                        summ.save()
>>>>>>> origin/master
                    
                    template = ResumeTemplate.objects.create(title=title, description=description)
                    introduction = Introduction.objects.create(user=request.user, template=template)
                    exp = Experience.objects.create(user=request.user, template=template)
                    create_resume_template(request, sections, template, introduction, exp)

                    #create Site
                    website = Website.objects.create(user=request.user,template=template)
                    website.domain = domain
                    website.template = template
                    website.description = description
                    website.save()
                    
                    response_data = {}
                    response_data['redirect'] = "/accounts/sites";
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
        else:
            #if no template selected and not a ajax response
            return HttpResponseRedirect("/sites/selectTemplate?error=1")

    return render(request, "website/createSite.html",locals())

<<<<<<< HEAD

def create_resume_template(request, sections, template, introduction, exp):
    print "what is going on"
    #template = ResumeTemplate.objects.create(title=request.POST.get('title'),description=request.POST.get('description'))
    template.path = "website/resumeTemplate.html"
    template.author = request.POST.get('author')
    template.save()

    if varExists(request,'summary'):
        summ = Post.objects.create(user=request.user,template=template)
        summ.title = "About Me"
        summ.content = request.POST.get('summary')
        summ.save()
                    
    #introduction
   # introduction = Introduction.objects.create(user=request.user,template=template)
    save = False
    if varExists(request,'name'):
        introduction.title = request.POST.get('name') 
        save = True
    if varExists(request,'education'):
        introduction.education = request.POST.get('education') 
        save = True
    if arrayExists(request,'majors'):
        introduction.majors = request.POST.get('majors') 
        save = True
    if arrayExists(request,'languages'):
        introduction.languages = request.POST.get('languages')
        save = True
    if varExists(request,'gpa'):
        introduction.gpa = request.POST.get('gpa')
        save = True
    if save:
        introduction.classes += " gray-bg"
        introduction.save()
    else:
        introduction.delete()


    #create experience section
    save = False
   # exp = Experience.objects.create(user=request.user,template=template)
    if arrayExists(request,'skills'):
        exp.skills = request.POST.get('skills')
        save = True
    if varExists(request,'experience'):
        exp.content = request.POST.get('experience')
        save = True
    if save:
        exp.title = "Experience"
        exp.save()
    else:
        exp.delete()
                        

    #create sections
    section = None 
    for i in range(len(sections)):
        if i % 2 == 0:
            section = Post.objects.create(user=request.user, template=template)
            section.title = sections[i]
            if i % 4 == 0:
                section.classes += " gray-bg"
        else:
            section.content = sections[i]
            section.save()


@login_required
def selectTemplate(request):
=======
@login_required
def selectTemplate(request):
    if 'error' in request.GET:
        template_error = True 
>>>>>>> origin/master
    return render(request, "website/selectTemplate.html", locals())
