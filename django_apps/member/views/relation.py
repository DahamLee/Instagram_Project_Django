from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST

User = get_user_model()


@require_POST
@login_required
def follow_toggle(request, user_pk):
    next = request.GET.get('next')

    target_user = get_object_or_404(User, pk=user_pk)
    request.user.follow_toggle(target_user)
    if next:
        return redirect(next)
    return redirect('member:profile', user_pk=user_pk)
