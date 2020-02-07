from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^loginpage$', views.login_page),
    url(r'^login$', views.login),
    url(r'^wishes$',    views.wishes),
    url(r'^wishes/new$',    views.wishes_new),
    url(r'^wishes/logout$',   views.wishes_logout),
    url(r'^wishes/create$',    views.wishes_create),
    url(r'^wishes/new/logout$',  views.wishes_new_logout),
    url(r'^wishes/remove/(?P<id>\d+)$',  views.wishes_remove),
    url(r'^wishes/edit/(?P<id>\d+)$',   views.wishes_edit_id),
    url(r'^wishes/update/(?P<id>\d+)$',    views.wishes_update_id),
    url(r'^wishes/granted/(?P<id>\d+)$',   views.wishes_granted_id),
    url(r'^wishes/like/(?P<id>\d+)$',   views.wishes_like_id)                 
]