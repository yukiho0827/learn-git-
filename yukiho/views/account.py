from django.shortcuts import render, redirect, HttpResponse
from yukiho import models
from datetime import datetime
from yukiho.utils.pagination import Pagination
from django import forms
from django.core.validators import ValidationError
from yukiho.utils.form import DepartModelForm, LoginForm
from yukiho.utils.code import check_code
from io import BytesIO


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        input_code = form.cleaned_data.pop('code')


