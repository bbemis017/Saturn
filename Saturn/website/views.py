from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from website.models import Website
from website.models import Template, ResumeTemplate, CourseTemplate, PageLinks
from website.forms import CreateSiteForm,CreateTemplateForm,CreateResumeTemplateForm, CreateCourseTemplateForm, DeleteSiteForm
from accounts.models import Accounts
from section.models import Introduction, Summary, Section, Post, Experience, About
from website.create import Create
from website.manage import Manage
from accounts.constants import ErrorCode
from django.utils.encoding import smart_str


import json



def displaySite(request,domain):
    website = Website.objects.get(domain=domain)

    #slightly more convenient variables
    template = website.template
    if template.path == "website/resumeTemplate.html":
        template = template.resumetemplate
    elif template.path == "website/courseTemplate.html":
        template = template.coursetemplate
        links = PageLinks.objects.filter(fromSite=website)


    sections = Section.objects.filter(template=template, user=website.user)

    return render(request,template.path,locals())

@login_required
def downloadSite(request,domain):

    website = Website.objects.get(domain=domain)
    template = website.template

    sections = Section.objects.filter(template=template, user=website.user)

    '''
    if template.path != "website/resumeTemplate.html":
        template.path = "website/courseTemplateDownload.html" 
    else:
        template.path = "website/resumeTemplateDownload.html" 
    '''
    download = True
    response = render(request, template.path, locals())
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(template.path)
    response['X-Sendfile'] = smart_str(template.path)

    return response

def varExists(request,string):
    if string in request.POST and request.POST.get(string) != '':
        return True
    else:
        return False

def createSite_validation(request, response_data):
    #this method checks the necessary fields for createSite
    #check essentials
    if not varExists(request,'domain'):
        response_data['domain_missing'] = 1
        response_data['error'] = 1
    if not varExists(request,'title'):
        response_data['title_missing'] = 1
        response_data['error'] = 1
    return response_data

def submitSite(request, response_data):
    #this method extracts the necessary info and submit them
    domain = request.POST.get('domain')
    title = request.POST.get('title')
    author = request.POST.get('author')
    description = request.POST.get('description')

    sections = {} 

    #check if site exists
    if not Website.objects.filter(domain=domain).exists():
        template = None
        # will not work until js is updated
        if 'courseTemplate' in request.POST: 
            template = create_course_template(request)
            print "course"
        elif 'resumeTemplate' in request.POST:
            template = create_resume_template(request)
            print "resume"

        createSections(request,request.user,template)

        #create Site
        website = Website.objects.create(user=request.user,template=template)
        website.domain = domain
        website.template = template
        website.description = description
        website.save()

        if 'link_domains' in request.POST:
            links = request.POST.get('link_domains')
            Create.pageLinks(request.user,template,website,links)

        response_data = {}
        response_data['redirect'] = "/accounts/sites";
        return response_data
    else:
        #error
        errorDomainExists = True
        response_data['error'] = 1
        return response_data

@login_required
def getSiteData(request):
    if request.is_ajax():
        domain = request.POST.get('domain')
        template = request.POST.get('template')
        print template

        data = {}

        #invalid domain and user combination then return error
        website = Website.objects.filter(domain=domain,user=request.user)
        if not website.exists():
            data = {'error' : 'INVALID'}
            return JsonResponse(data)
        website = website[0]

        data = {'domain': website.domain, 'title' : website.template.title,
                'description' : website.description }

        data = Manage.getSectionData(website.template,data)

        #TODO: work on getting additional information from templates
        if template == 'resume':
            data['template'] = 'resume'
            data['author'] = website.template.resumetemplate.author
            data.update( Manage.getIntroData(website.template) )
            data.update( Manage.getSummaryData(website.template) )
            data.update( Manage.getExperienceData(website.template) )
        elif template == 'course':
            data['template'] = 'course'
            data['author'] = website.template.coursetemplate.author
            data.update( Manage.getPostContent(website.template,Create.ABOUT_COURSE) )
            data.update( Manage.getListSectionData(website.template, Create.INSTRUCTORS) )
            data.update( Manage.getListSectionData(website.template, Create.GRADES) )
            data.update( Manage.getListSectionData(website.template, Create.TAS) )
            data.update( Manage.getListSectionData(website.template, Create.EXAMS) )
            data.update( Manage.getPostContent(website.template, Create.COURSE_SYLLABUS) )
            data = Manage.getPageLinks(website,data)
            print "course"
            print data


        return JsonResponse(data)


@login_required
def editPage(request):

    #if site is not specified redirect to Sites page
    if 'domain' not in request.GET:
        return HttpResponseRedirect("/accounts/sites")

    editDomain = request.GET.get('domain')

    #invalid domain and user combination then redirect to sites page
    editWebsite = Website.objects.filter(domain=editDomain,user=request.user)
    if not editWebsite.exists():
        return HttpResponseRedirect("/accounts/sites")

    editWebsite = editWebsite[0]
    editTemplate = ""

    try:
        editWebsite.template.resumetemplate
    except editWebsite.template.DoesNotExist:
        courseTemplateSelect = True
        editTemplate = "course"
        sites = Website.objects.filter(user=request.user)
    else:
        resumeTemplateSelect = True
        editTemplate = "resume"



    return render(request,"website/createSite.html",locals())

@login_required
def createSite(request):
    #for information displayed on navigation bar
    account = Accounts.objects.get(user=request.user)

    if request.method == "POST":
        print request.POST
        #determine the type of form to display
        if 'resumeTemplateSelect' in request.POST:
            resumeTemplateSelect = True
        elif 'courseTemplateSelect' in request.POST:
            courseTemplateSelect = True
            sites = Website.objects.filter(user=request.user)

        elif request.is_ajax():

            response_data = {}

            if 'submit' in request.POST:

                response_data = createSite_validation(request, response_data)
                if 'error' in response_data:
                    return JsonResponse(response_data)

                response_data = submitSite(request, response_data);
                return JsonResponse(response_data)

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

def editSite(request) :
    account = Accounts.objects.get(user=request.user)

    if request.method == "POST":
        if 'submit' in request.POST:
            #check essentials
            if not varExists(request,'domain'):
                error_code = ErrorCode.DOMAIN_MISSING
                return JsonResponse({'error_code': error_code})
            if not varExists(request,'title'):
                error_code = ErrorCode.TITLE_MISSING
                return JsonResponse({'error_code': error_code})

            #no error occurs
            #create sections
            domain = request.POST.get('domain')
            title = request.POST.get('title')
            author = request.POST.get('author')
            description = request.POST.get('description')

            #determine the type of form to display
            website = Website.objects.get(user=request.user, domain=domain)
            #delete sections
            sections = Section.objects.filter(template=website.template)

            if sections.exists():
                sections.delete()
            #if website.template.exists():
                website.template.delete()
            pages = PageLinks.objects.filter(fromSite=website)
            if pages.exists():
                pages.delete()



            sections = {} 

            #check and assign variables


            template = None
            # will not work until js is updated
            if 'courseTemplate' in request.POST: 
                template = create_course_template(request)
                print "course"
            elif 'resumeTemplate' in request.POST:
                template = create_resume_template(request)
                print "resume"

            createSections(request,request.user,template)

            #create Site
            website.domain = domain
            website.template = template
            website.description = description
            website.save()

            if 'link_domains' in request.POST:
               links = request.POST.get('link_domains')
               Create.pageLinks(request.user,template,website,links)

               response_data = {}
               response_data['redirect'] = "/accounts/sites";
               return JsonResponse(response_data);

    #return render(request, "website/createSite.html",locals())
    return JsonResponse({ 'redirect' : "/accounts/sites" } )


def create_course_template(request):

    template = CourseTemplate.objects.create()
    template.title = request.POST.get('title')
    template.description = request.POST.get('description')
    template.path = "website/courseTemplate.html"
    template.author = request.POST.get('author')
    template.save() 

    aboutCourse = request.POST.get('aboutCourse')
    about = Create.aboutSection(request.user,template,"About",aboutCourse)

    instructorList = request.POST.get('instructors')
    if Create.arrayExists(instructorList):
        instructors = Create.listSection(request.user,template,Create.INSTRUCTORS,instructorList)

    gradeList = request.POST.get('grades')
    if Create.arrayExists(gradeList):
        grades = Create.listSection(request.user,template,Create.GRADES,gradeList)

    taList = request.POST.get('tas')
    if Create.arrayExists(taList):
        tas = Create.listSection(request.user,template,Create.TAS,taList)

    examList = request.POST.get('exams')
    if Create.arrayExists(examList):
        exams = Create.listSection(request.user,template,Create.EXAMS,examList)

    syllabus = request.POST.get('syllabus')
    syllabusSection = Create.syllabusSection(request.user,template,syllabus)

    return template



def create_resume_template(request):
    if varExists(request,'summary'):
        summary = request.POST.get('summary')

    template = ResumeTemplate.objects.create(title=request.POST.get('title'))
    template.description = request.POST.get('description')
    template.path = "website/resumeTemplate.html"
    template.author = request.POST.get('author')
    template.save()




    Create.aboutSection(request.user, template, "About me", request.POST.get('summary'))
    


    #introduction
    introduction = Introduction.objects.create(user=request.user,template=template)
    save = False
    if varExists(request,'name'):
        introduction.title = request.POST.get('name') 
        save = True
    if varExists(request,'education'):
        introduction.education = request.POST.get('education') 
        save = True
    if Create.arrayExists(request.POST.get('majors')):
        introduction.majors = request.POST.get('majors') 
        print "save majors"
        save = True
    if Create.arrayExists(request.POST.get('languages')):
        introduction.languages = request.POST.get('languages')
        save = True
    if varExists(request,'gpa'):
        introduction.gpa = request.POST.get('gpa')
        save = True
    if save:
        introduction.title = "Education"
        introduction.classes += " gray-bg"
        introduction.save()
    else:
        introduction.delete()


    #create experience section
    save = False
    exp = Experience.objects.create(user=request.user,template=template)
    if Create.arrayExists(request.POST.get('skills')):
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

    return template

def createSections(request,user,template):
    section = None

    if Create.arrayExists(request.POST.get('sections')):
        sections = json.loads(request.POST.get('sections') )
    else:
        return False

    #create sections
    blank = True 
    for i in range(len(sections)):
        if i % 2 == 0:
            section = Post.objects.create(user=user,template=template)
            section.title = sections[i]
            if section.title:
                blank = False
            if i % 4 == 0:
                section.classes += " gray-bg"
        else:
            section.content = sections[i]
            if section.content:
                blank = False
            if blank:
                section.delete()
            else:
                blank = True
                section.save()


@login_required
def selectTemplate(request):
    if 'error' in request.GET:
        template_error = True 
    return render(request, "website/selectTemplate.html", locals())
