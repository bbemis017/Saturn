from section.models import(
        Section,
        Introduction,
        Experience,
        Post,
        List,
        About
        )
from website.models import PageLinks
from website.create import Create
import json

class Manage(object):

    @staticmethod
    def getIntroData(template):
        intro = Introduction.objects.filter(template=template)
        data = {}

        if intro.exists():
            intro = intro[0]
            data['name'] = intro.title
            data['education'] = intro.education
            data['majors'] = intro.majors
            data['languages'] = intro.languages
            data['gpa'] = intro.gpa

        return data

    @staticmethod
    def getSummaryData(template):
        summaries = About.objects.filter(template=template)
        data = {}

        if summaries.exists():
            data['summary'] = summaries[0].content
            if summaries[0].image != None:
                data['summaryImage'] = summaries[0].image.content.name

        return data
    @staticmethod
    def getAboutData(template):
        sections = About.objects.filter(template=template)
        data = {}

        if sections.exists():
            data['About'] = sections[0].content
        return data

    @staticmethod
    def getExperienceData(template):
        exp = Experience.objects.filter(template=template)
        data = {}

        if exp.exists():
            exp = exp[0]
            data['experience'] = exp.content 
            data['skills'] = exp.skills

        return data

    @staticmethod
    def getSectionData(template,data):
        sections = Post.objects.filter(template=template)
        sections = sections.exclude(title="About Me")
        sections = sections.exclude(title=Create.ABOUT_COURSE)
        sections = sections.exclude(title=Create.COURSE_SYLLABUS)
        sections = sections.exclude(title=Create.INSTRUCTORS)
        sections = sections.exclude(title=Create.GRADES)
        sections = sections.exclude(title=Create.TAS)
        sections = sections.exclude(title=Create.EXAMS)

        sectionList = [] 
        for section in sections:
           sectionList.append(section.title)
           sectionList.append(section.content)
        data['sections'] = json.dumps( sectionList )
        return data

    @staticmethod
    def getPageLinks(website,data):
        links = PageLinks.objects.filter(fromSite=website)

        linkList = []

        for link in links:
            linkList.append( link.toSite.domain )

        data['links'] = json.dumps( linkList )
        return data

    @staticmethod
    def getPostContent(template,title):
        try:
            section = Post.objects.get(template=template,title=title)
        except Post.DoesNotExist:
            return {}

        return { title : section.content }

    @staticmethod
    def getListSectionData(template,title):
        try:
            section = List.objects.get(template=template,title=title)
        except List.DoesNotExist:
            return {}
        
        return { title : section.items }

