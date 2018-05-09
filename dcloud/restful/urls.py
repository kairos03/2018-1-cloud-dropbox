from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from restful import views

urlpatterns = [
    url(r'^files/$', views.FileList.as_view(), name='file-list'),
    url(r'^files/(?P<pk>[0-9]+)/$', views.FileDetail.as_view(), name='file-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)