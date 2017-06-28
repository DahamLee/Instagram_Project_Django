from django.db import models

__all__ = (
    'Video',
)


class Aa(models.Manager):
    def create_from_search_result(self, item):
        youtube_videoId = item.get('id').get('videoId')
        youtube_thumbnails = item.get('snippet').get('thumbnails').get('default').get('url')
        youtube_title = item.get('snippet').get('title')
        youtube_description = item.get('snippet').get('title')
        video, video_created = Video.objects.get_or_create(

            youtube_videoId=youtube_videoId,

            defaults={

                'youtube_title': youtube_title,
                'youtube_description': youtube_description,
                'youtube_thumbnails': youtube_thumbnails,

            })
        print('Video({}) is {}'.format(
            video.youtube_title,
            'created' if video_created else 'already exist'

        ))

        return video


class Video(models.Model):

    youtube_videoId = models.CharField(max_length=100, unique=True)
    youtube_title = models.CharField(max_length=100)
    youtube_description = models.TextField(blank=True)
    youtube_thumbnails = models.CharField(max_length=100)

    objects = Aa()

    def __str__(self):
        return self.youtube_title
