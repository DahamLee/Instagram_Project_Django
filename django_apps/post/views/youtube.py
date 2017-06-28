from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from post.models import Video, Post, Comment
from utils import youtube

__all__ = (
    'youtube_search',
    'post_create_with_video',
)


def youtube_search(request, q=None):
    context = dict()
    q = request.GET.get('q')

    if q:
        data = youtube.search(q)
        videos = []
        for item in data['items']:
            videos.append(Video.objects.create_from_search_result(item))
        # re_pattern = ''.join(['(?=.*{}'.format(item) for item in q.split()])
        # videos = Video.objects.filter(
        #     Q(youtube_title__iregex=re_pattern) |
        #     Q(youtube_description__iregex=re_pattern)
        # )
        context['videos'] = videos
    return render(request, 'post/youtube_search.html', context)


    #     youtube_ids = response.json().get('items')
    #
    #     for youtube_id in youtube_ids:
    #         search_word = q
    #         youtube_videoId = youtube_id.get('id').get('videoId')
    #         youtube_thumbnails = youtube_id.get('snippet').get('thumbnails').get('default').get('url')
    #         youtube_title = youtube_id.get('snippet').get('title')
    #         youtube_description = youtube_id.get('snippet').get('title')
    #         videoid, videoid_created = Video.objects.get_or_create(
    #
    #             youtube_videoId=youtube_videoId,
    #
    #             defaults={
    #                 'search_word': search_word,
    #                 'youtube_title': youtube_title,
    #                 'youtube_description': youtube_description,
    #                 'youtube_thumbnails': youtube_thumbnails,
    #
    #             })
    #
    #         # or연산
    #         # re_pattern = '|'.join([r'(?=.*{})'.format(item) for item in q.split()])
    #
    #         # and연산
    #         re_pattern = ''.join([r'(?=.*{})'.format(item) for item in q.split()])
    #         videos = Video.objects.filter(Q(youtube_title__regex=r'{}'.format(re_pattern)) |
    #                                       Q(youtube_description__regex=r'{}'.format(re_pattern)))
    #
    #         # videos.filter(title__contains='패스트캠퍼스').filter(title__contains='웹').filter(title__contains='프로그래밍')
    #
    #         context = {
    #             'videos': videos,
    #             're_pattern': re_pattern,
    #         }
    #
    # else:
    #     context = {}
    # return render(request, 'post/youtube_search.html', context)


@require_POST
@login_required
def post_create_with_video(request):
    video_pk = request.POST['video_pk']

    video = get_object_or_404(Video, pk=video_pk)

    post = Post.objects.create(
        author=request.user,
        video=video,
    )
    post.my_comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=video.youtube_title,
    )

    post_pk = post.pk

    return redirect('post:post_detail', post_pk)
