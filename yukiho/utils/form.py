from yukiho import models
from django.core.validators import ValidationError
from django import forms
from .bootstrap_modelform import BootStrapModelForm, BootStrapForm
from yukiho.utils import encrypt


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


class LoginForm(BootStrapForm,forms.Form):
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

