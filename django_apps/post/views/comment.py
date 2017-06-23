from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST

from post.decorators import comment_owner
from post.forms import CommentForm
from ..models import Post, Comment

# 자동으로 Django에서 인증에 사용하는 User모델클래스를 리턴
#   https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.get_user_model
User = get_user_model()

__all__ = (
    'comment_create',
    'comment_modify',
    'comment_delete',
)


@require_POST
@login_required
def comment_create(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        next = request.GET.get('next')
        print('next: {}========='.format(next))
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            form.save()
        else:

            result = '<br>'.join(['<br>'.join(v) for v in form.errors.values()])
            messages.error(request, result)

        if next:
            return redirect(next)
        return redirect('post:post_detail', post_pk=post.pk)


def comment_modify(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    next = request.GET.get('next')
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        form.save()
        if next:
            return redirect(next)
        return redirect('post:post_detail', post_pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form':form,
    }
    return render(request, 'post/comment_modify.html', context)

@comment_owner
@require_POST #get요청이 왔을때 아무일도 안한다
@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    comment.delete()
    return redirect('post:post_detail', post_pk=post.pk)


def post_anyway(request):
    return redirect('post:post_list')


def main(request):
    return redirect('post:post_list')
