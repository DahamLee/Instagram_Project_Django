from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.


def login(request):
    if request.method == 'POST':
        id = request.POST.get('ID', '')
        password = request.POST.get('PASSWORD', '')
        print()
        user = authenticate(username= id, password = password)
        if user is not None:
            return redirect('post:post_list')
        else:
            return HttpResponse('Login invalid')

    else:
        return render(request, 'member/login.html')
