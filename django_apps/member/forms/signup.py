from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class SignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', ' : : ')
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '사용자 아이디를 입력하세요'
            }
        ),
        max_length=24,
    )

    nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '닉네임은 유일해야 합니다'
            }

        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요'
            }
        ))

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요'
            }
        ))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Username already exists'
            )
        return username

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if nickname and User.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError(
                'Nickname already exist'
            )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'different password'
            )

    def create_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_date['password2']
        nickname = self.cleaned_data['nickname']

        user = User.objects.create_user(
            username=username,
            password=password,
            nickname=nickname,
        )
        return user

# class UserCreationForm(forms.ModelForm):
#     pass