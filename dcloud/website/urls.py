from django.conf.urls import url
from django.shortcuts import redirect
from website import views, auth_views

urlpatterns = [

    url(r'^accounts/signup/$', auth_views.signup, name='signup'),
    url(r'^accounts/delete_account/$', auth_views.delete_account, name='delete_account'),
    url(r'^accounts/delete_account_success/$', auth_views.delete_account_success, name='delete_account_success'),

    # blog
    url(r'^$', views.home, name='home'),
    url(r'^list/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/)*)$', views.file_list, name='file_list'),
    url(r'^upload/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/)*)$', views.file_upload, name='file_upload'),
    url(r'^download/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/)*)$', views.file_download, name='file_download'),
    url(r'^delete/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/)*)$', views.file_delete, name='file_delete'),
    url(r'^make_folder/(?P<path>([\w\s가-힣.\`\'\˜\=\+\#\ˆ\@\$\&\-\.\(\)\{\}\;\[\]]*/)*)$', views.make_folder, name='make_folder'),
]