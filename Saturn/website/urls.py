from django.conf.urls import url
from website import views

urlpatterns = [

        #this is the only url that works in this file
        url(r'(?P<domain>[-\w]+)',views.displaySite),
]
