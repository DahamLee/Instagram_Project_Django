from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import UserEditForm

__all__ = (
    'profile',
    'profile_edit',

)
User = get_user_model()


def profile(request, user_pk=None):
    NUM_POST_PER_PAGE = 3
    page = request.GET.get('page', 1)

    try:
        page = int(page) if int(page) > 1 else 1

    except ValueError:
        page = 1
    except Exception as e:
        page = 1
        print(e)

    if user_pk:
        cur_user = get_object_or_404(User, pk=user_pk)
    else:
        cur_user = request.user

    posts = cur_user.post_set.order_by('-created_date')[:page * NUM_POST_PER_PAGE]
    post_count = cur_user.post_set.count()

    next_page = page + 1 if post_count > page * NUM_POST_PER_PAGE else None

    context = {
        'cur_user': cur_user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page': next_page,
    }

    return render(request, 'member/profile.html', context)


def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('member:my_profile')
    else:
        form = UserEditForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'member/profile_edit.html', context)
