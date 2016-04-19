from section.models import(
        Section,
        Post,
        List,
	 About
        )
from website.models import(
        PageLinks,
        Website
        )

import json

class Create(object):


    @staticmethod
    def aboutSection(user, template, title, description):
        if description:
            section = About.objects.create(user=user,template=template)
            section.title = title;
            section.content = description
            section.save()
            return section
        else:
            return False

            

    @staticmethod
    def listSection(user, template, title, string):
        valid = False
        section = List.objects.create(user=user,template=template)
        if title:
            valid = True
            section.title = title
        if arrayExists(string):
            valid = True
            section.items = string
        if valid:
            section.save()
            return section
        else:
            section.delete()
            return False
    
    @staticmethod
    def syllabusSection(user, template, string):
        if string:
            section = Post.objects.create(user=user, template=template)
            section.content = string
            section.title = "Syllabus"
            section.save()
            return section
        else:
            return False

    @staticmethod
    def pageLinks(user, template,currentWebsite, string):
        if Create.arrayExists(string):
            links = json.loads( string )
            for link in links:
                w = Website.objects.get(domain=link,user=user)
                pl = PageLinks.objects.create(fromSite=currentWebsite,toSite=w)
                pl.save()

    '''
    checks whether or not an array of values exist inside
    of the string
    '''
    @staticmethod
    def arrayExists(string):
        variable = ''
        try:
            variable = json.loads( string )
        except ValueError, e:
            return False
        if len(variable) == 1 and variable[0] == '':
            return False 
        elif len(variable):
            return True
        else:
            return False

