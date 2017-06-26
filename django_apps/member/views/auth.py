import re

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, \
    login as django_login, \
    logout as django_logout
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
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
    code = request.GET.get('code')

    app_access_token = '{}|{}'.format(
        settings.FACEBOOK_APP_ID,
        settings.FACEBOOK_SECRET_CODE,
    )

    class GetAccessTokenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]['error']
            self.message = error_dict['message']
            self.is_valid = error_dict['is_valid']
            self.scopes = error_dict['scopes']
            self.code = error_dict['code']

    class DebugTokenException(Exception):
        def __init__(self, *args, **kwargs):
            error_dict = args[0]['data']['error']
            self.code = error_dict['code']
            self.message = error_dict['message']

    def add_message_and_redirect_referer():
        error_message_for_user = 'Facebook login error'
        messages.error(request, error_message_for_user)
        return redirect(request.META['HTTP_REFERER'])

    def get_access_token(code):

        url_access_token = 'https://graph.facebook.com/' \
                           'v2.9/oauth/access_token?client_id={app-id}&redirect_uri=' \
                           '{redirect-uri}&client_secret={app-secret}&code={code-parameter}'
        redirect_uri = '{}://{}{}'.format(
            request.scheme,
            request.META['HTTP_HOST'],
            request.path,
        )

        url_access_token_params = {
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': redirect_uri,
            'client_secret': settings.FACEBOOK_SECRET_CODE,
            'code': code,
        }
        response = requests.get(url_access_token, params=url_access_token_params)
        result = response.json()
        if 'access_token' in result:
            return result['access_token']

        elif 'error' in result:

            raise Exception(result['error'])
            # error_message = 'Facebook login error\n type: {}\n messages: {}'.format(
            #     result['error']['type'],
            #     result['error']['message']
            # )

        else:
            raise Exception('Unknown error')

    def debug_token(token):
        url_debug_token = 'https://graph.facebook.com/debug_token?'
        url_debug_token_params = {
            'input_token': token,
            'access_token': app_access_token
        }
        response = requests.get(url_debug_token, url_debug_token_params)
        result = response.json()
        if 'error' in result['data']:
            raise Exception(result['data']['error'])
        else:
            return result

    def get_user_info(user_id, token):
        url_user_info = 'https://graph.facebook.com/v2.9/{user_id}'.format(user_id=user_id)
        url_user_info_params = {
            'access_token': token,
            'fields': ','.join([
                'id',
                'name',
                'first_name',
                'last_name',
                'picture.type(large)',
                'gender',

            ])
        }
        response = requests.get(url_user_info, params=url_user_info_params)
        result = response.json()
        return result

    if not code:
        return add_message_and_redirect_referer()
    try:

        access_token = get_access_token(code)

        debug_result = debug_token(access_token)

        user_info = get_user_info(user_id=debug_result['data']['user_id'], token=access_token)
        user = User.objects.get_or_create_facebook_user(user_info)


        django_login(request, user)
        return redirect(request.META['HTTP_REFERER'])

    except GetAccessTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()
    except DebugTokenException as e:
        print(e.code)
        print(e.message)
        return add_message_and_redirect_referer()
