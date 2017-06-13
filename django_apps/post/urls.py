from django.conf.urls import url

from post import views

app_name = 'post'

urlpatterns = [
    url(r'^$', views.index),
    url(r'^list/', views.post_list, name='post_list'),

    # 정규표현식에서 매칭 된 그룹을 위치인수로 반환하는 방법
    # url(r'^(\d+)/$',  views.post_detail),

    # 정규표현식에서 매칭 된 그룹을 키워드인수로 반환하는 방법
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),

    url(r'^create/$', views.post_create, name='post_create'),



    url(r'^.*/$', views.post_anyway, name='post_anyway'),
]
