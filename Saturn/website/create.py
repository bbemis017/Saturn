from section.models import(
        Section,
        Post,
        List
        )

import json

class Create(object):


    @staticmethod
    def aboutSection(user, template, description):
        if description:
            section = Post.objects.create(user=user,template=template)
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

    '''
    checks whether or not an array of values exist inside
    of the string
    '''
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

