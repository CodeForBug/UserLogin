from django import forms
from django.contrib.auth.models import User
import re


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):  # 注册

    username = forms.CharField(label="Username", max_length=50)
    email = forms.EmailField(label="Email", )
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password Confirmation", widget=forms.PasswordInput)

    # Use clean methods to define custom validation rules
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 6:
            raise forms.ValidationError("用户名至少6个字符!")
        elif len(username) > 50:
            raise forms.ValidationError("用户名过长!")
        else:
            filter_result = User.objects.filter(username__exact=username)  # 判断用户名是否存在
            if len(filter_result) > 0:
                raise forms.ValidationError("用户名已存在！")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)  # 判断邮箱是否存在
            if len(filter_result) > 0:
                raise forms.ValidationError("邮箱已存在！")
        else:
            raise forms.ValidationError("邮箱不合法！")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 6:
            raise forms.ValidationError("密码过短！")
        elif len(password1) > 20:
            raise forms.ValidationError("密码过长！")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不符合，请重新输入！")

        return password2


class LoginForm(forms.Form):  # 登录

    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError("邮箱不存在！")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError("账号不存在！")

        return username

