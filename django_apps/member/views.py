from django.contrib.auth import authenticate, get_user_model, \
    login as django_login, \
    logout as django_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

User = get_user_model()


def login(request):
    if request.method == 'POST':
        # id = request.POST.get('ID', '')
        # password = request.POST.get('PASSWORD', '')
        # print('{}'.format(User.objects.get(id=2).username))
        # print('id = {}, password = {}'.format(id, password))
        # user = authenticate(username= id, password = password)

        username = request.POST['ID']
        password = request.POST['PASSWORD']
        user = authenticate(
            request,
            username=username,
            password=password, )

        if user is not None:
            django_login(request, user)
            return redirect('post:post_list')
        else:
            return HttpResponse('Login credentials invalid')

    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        else:
            return render(request, 'member/login.html')


def logout(request):
    django_logout(request)
    return redirect('post:post_list')
