import requests
from django.db.models import Q
from django.shortcuts import render

from post.models import Video

__all__ = (
    'youtube_search',
)


def youtube_search(request):
    url_api_search = 'https://www.googleapis.com/youtube/v3/search'
    q = request.GET.get('q')

    if q:
        search_params = {
            'part': 'snippet',
            'key': 'AIzaSyAkZCCx5l_Rg68Mc3Bs83Ax--b44gnaaIU',
            'q': q,
            'maxResults': 10,
            'type': 'video',

        }

        response = requests.get(url_api_search, params=search_params)

        youtube_ids = response.json().get('items')

        for youtube_id in youtube_ids:
            search_word = q
            youtube_videoId=youtube_id.get('id').get('videoId')
            youtube_thumbnails = youtube_id.get('snippet').get('thumbnails').get('default').get('url')
            youtube_title = youtube_id.get('snippet').get('title')
            youtube_description = youtube_id.get('snippet').get('title')
            videoid, videoid_created = Video.objects.get_or_create(
                search_word=search_word,
                youtube_videoId=youtube_videoId,
                youtube_title=youtube_title,
                youtube_description=youtube_description,
                youtube_thumbnails=youtube_thumbnails,
            )
        videos = Video.objects.filter(Q(youtube_title__contains=q)|Q(youtube_description__contains=q))

        context = {
            'videos': videos,
        }

    else:
        context = {}
    return render(request, 'post/youtube_search.html', context)
