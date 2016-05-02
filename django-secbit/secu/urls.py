from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.login, name='login'),
    url(r'^$', views.index, name='index'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'close/$', views.close, name='close'),
    url(r'transfer/$', views.transfer, name='transfer'),
    url(r'view_users/$', views.ViewUser.as_view(), name='view_users'),
]
