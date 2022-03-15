from django.shortcuts import render, redirect, HttpResponse
from yukiho import models
from datetime import datetime
from yukiho.utils.pagination import Pagination
from django import forms
from django.core.validators import ValidationError
from yukiho.utils.form import DepartModelForm, LoginForm, UserModelForm
from yukiho.utils.code import check_code
from io import BytesIO


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/manage')
    return render(request, 'user_add.html', {'form': form})


def user_edit(request, uid):
    row_object = models.UserInfo.objects.filter(id=uid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '未知错误'})
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/manage')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, uid):
    row_object = models.UserInfo.objects.filter(id=uid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '未知错误'})
    row_object.delete()
    return redirect('/user/manage')


def user_manage(request):
    search_data = request.GET.get('data', '')
    data_list = {}
    if search_data:
        # 根据字段名不同来设置
        data_list['user__contains'] = search_data

    queryset = models.UserInfo.objects.filter(**data_list)

    page_obj = Pagination(request, queryset)

    content = {
        'search_data': search_data,
        'user_list': page_obj.page_queryset,
        'page_list_string': page_obj.show_page(),
    }
    return render(request, 'user_manage.html', content)
