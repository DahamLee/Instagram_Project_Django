from django.conf.urls import url

from post import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/', views.post_list),
]