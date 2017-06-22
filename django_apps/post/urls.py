from django.conf.urls import url

from . import views

app_name = 'post'

urlpatterns = [
    url(r'^list/$', views.post_list, name='post_list'),

    # 정규표현식에서 매칭 된 그룹을 위치인수로 반환하는 방법
    # url(r'^(\d+)/$',  views.post_detail),

    # 정규표현식에서 매칭 된 그룹을 키워드인수로 반환하는 방법
    url(r'^(?P<post_pk>\d+)/$', views.post_detail, name='post_detail'),

    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<post_pk>\d+)/modify/$', views.post_modify, name='post_modify'),
    url(r'^(?P<post_pk>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^(?P<post_pk>\d+)/comment/create/$', views.comment_create, name='comment_create'),
    url(r'^(?P<post_pk>\d+)/like-toggle/$', views.post_like_toggle, name='post_like_toggle'),

    url(r'^comment/(?P<comment_pk>\d+)/modify/$', views.comment_modify, name='comment_modify'),
    url(r'^comment/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
    url(r'^tag/(?P<tag_name>\w+)/$', views.hashtag_post_list, name='hashtag_post_list'),



    url(r'^.*/$', views.post_anyway, name='post_anyway'),
]
