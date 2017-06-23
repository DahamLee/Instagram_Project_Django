from django.contrib.auth import get_user_model, \
    login as django_login, \
    logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import UserEditForm
from .forms import LoginForm
from .forms import SignupForm

# Create your views here.

User = get_user_model()


def login(request):
    if request.method == 'POST':
        # FORM클래스 미사용시
        # id = request.POST.get('ID', '')
        # password = request.POST.get('PASSWORD', '')
        # print('{}'.format(User.objects.get(id=2).username))
        # print('id = {}, password = {}'.format(id, password))
        # user = authenticate(username= id, password = password)
        # username = request.POST['username']
        # password = request.POST['password']



        # user = authenticate(
        #     request,
        #     username=username,
        #     password=password, )


        # if user is not None:
        #     django_login(request, user)
        #     return redirect('post:post_list')


        # FORM클래스 사용시
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            return redirect('post:post_list')

        else:
            return HttpResponse('Login credentials invalid')

    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':

        # 폼을 사용하지 않는 경우
        # user_id = request.POST['id']
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        #
        # if User.objects.filter(username=user_id).exists():
        #     return HttpResponse('이미 있는 id입니다')
        # elif password2 != password1:
        #     return HttpResponse('Password OK')
        #
        # user1 = User.objects.create_user(
        #     username=user_id,
        #     password=password1)
        #
        # django_login(request, user1)
        # return redirect('post:post_list')

        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.create_user()

            django_login(request, user)

            return redirect('post:post_list')
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)


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


@require_POST
@login_required
def follow_toggle(request, user_pk):
    next = request.GET.get('next')

    target_user = get_object_or_404(User, pk=user_pk)
    request.user.follow_toggle(target_user)
    if next:
        return redirect(next)
    return redirect('member:profile', user_pk=user_pk)


def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('member:my_profile')
    else:
        form = UserEditForm(instance=request.user)
        context = {
            'form':form
        }
        return render(request, 'member/profile_edit.html', context)
