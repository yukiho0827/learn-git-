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


def admin_manage(request):
    search_data = request.GET.get('data', '')
    data_list = {}
    if search_data:
        # 根据字段名不同来设置
        data_list['user__contains'] = search_data

    queryset = models.Admin.objects.filter(**data_list)

    page_obj = Pagination(request, queryset)

    content = {
        'search_data': search_data,
        'user_list': page_obj.page_queryset,
        'page_list_string': page_obj.show_page(),
    }
    return render(request, 'admin_manage.html', content)
