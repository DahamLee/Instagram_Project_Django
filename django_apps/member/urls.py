from django.conf.urls import url

from . import views

app_name = 'member'

urlpatterns = [
    url(r'^login/$', views.login, name='member_login'),
    url(r'^logout/$', views.logout, name='member_logout'),

]
