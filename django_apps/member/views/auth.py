from pprint import pprint

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, \
    login as django_login, \
    logout as django_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ..forms import LoginForm
from ..forms import SignupForm

# Create your views here.

User = get_user_model()

__all__ = (
    'login',
    'logout',
    'signup',
    'facebook_login',
)


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


def facebook_login(request):
    redirect_uri = '{}://{}{}'.format(
        request.scheme,
        request.META['HTTP_HOST'],
        request.path,
    )

    url_access_token = 'https://graph.facebook.com/' \
                       'v2.9/oauth/access_token?client_id={app-id}&redirect_uri=' \
                       '{redirect-uri}&client_secret={app-secret}&code={code-parameter}'

    code = request.GET.get('code')
    if code:
        url_access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
        }
        response = requests.get(url_access_token, params=url_access_token_params)
        result = response.json()
        pprint(result)