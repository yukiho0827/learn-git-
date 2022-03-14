from django.shortcuts import render, redirect, HttpResponse
from yukiho import models
from datetime import datetime
from yukiho.utils.pagination import Pagination
from django import forms
from django.core.validators import ValidationError
from yukiho.utils.form import DepartModelForm, LoginForm, AdminModelForm
from yukiho.utils.code import check_code
from io import BytesIO


def admin_add(request):
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'admin_add.html', {'form': form})
    form = AdminModelForm(data=request.POST)

    if form.is_valid():

        form.save()
        return redirect('/admin/manage')

    return render(request, 'admin_add.html', {'form': form})

