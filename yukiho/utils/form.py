from yukiho import models
from django.core.validators import ValidationError
from django import forms
from .bootstrap_modelform import BootStrapModelForm, BootStrapForm
from yukiho.utils import encrypt


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['user', 'password', 'age', 'gender', 'depart', 'create_time']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }


class DepartModelForm(BootStrapModelForm):
    class Meta:
        model = models.Department
        fields = '__all__'

    def clean_depart(self):
        depart = self.cleaned_data['depart']

        res = models.Department.objects.filter(depart=depart).exists()
        if res:
            raise ValidationError('部门重复')
        return depart


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = models.Admin
        fields = ['user', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_user(self):
        user = self.cleaned_data.get('user')
        res = models.Admin.objects.filter(user=user).exists()
        if res:
            raise ValidationError('重复的用户名')
        return user

    def clean_password(self):
        password = self.cleaned_data.get('password')
        md5_password = encrypt.md5(password)
        return md5_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm = encrypt.md5(self.cleaned_data.get('confirm_password'))
        if not password:
            return
        if confirm != password:
            raise ValidationError('两次输入的密码不一致,请重新输入。')


class LoginForm(BootStrapForm, forms.Form):
    user = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = encrypt.md5(pwd)
        return md5_pwd
