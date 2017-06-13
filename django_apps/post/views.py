from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from post.models import Post

User = get_user_model()


def index(request):
    return HttpResponse('Hello World')


def post_list(request):
    # 모든 post목록을 'post'라는 key로
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # 가져오는 과정에서 예외처리를 한다 (Model.DeosNotExist)
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        # return HttpResponseNotFound('Post not found, detail: {}'.format(e))

        # return redirect('post:post_list')

        url = reverse('post:post_list')
        return HttpResponseRedirect(url)

    # render함수는 django.template.loader.get_template함수와
    # django.http.HttpResponse함수를 축약해 놓은 shortcut이다

    # Django가 템플릿을 검색할 수 있는 모든 디렉토리를 순회하며
    # 인자로 주어진 문자열값과 일치하는 템플릿이 있는 지 확인 후
    # 결과를 리턴 (django.template.backends.dkango.Template
    template = loader.get_template('post/post_detail.html')

    # dict형 변수 context 'post'키에 post(Post 객체를 할당
    context = {
        'post': post,
    }

    rendered_string = template.render(context=context, request=request)
    return HttpResponse(rendered_string)


def post_create(request):
    if request.method == 'POST':
        # get_user_model을 이용해서 얻은 User클래스(Django에서 인증에 사용하는 유저모델)에서 유저 한명을 가져온다
        user = User.objects.first()
        # 새 Post객체를 생성하고 DB에 저장
        post = Post.objects.create(
            author=user,

            # request.FILES에서 파일 가져오기
            # 'file'은 POST요청시 input[type="file"]이 가진 name 속성
            photo=request.FILES['file'],

        )
        # dict.get 함수
        comment_string = request.POST.get('comment', '')

        if comment_string:
            post.comment_set.create(
                author=user,
                content = comment_string,
            )


        return redirect('post:post_detail', post_pk=post.pk)
    else:
        return render(request, 'post/post_create.html')


def post_anyway(request):
    return redirect('post:post_list')
