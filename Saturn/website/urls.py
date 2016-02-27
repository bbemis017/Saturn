from django.conf.urls import url
from website import views

urlpatterns = [
        #used for testing template only
        url(r'^test/$',views.testTemplate),
]
