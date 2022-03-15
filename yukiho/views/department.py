from django.shortcuts import render, redirect, HttpResponse
from yukiho import models
from yukiho.utils.form import DepartModelForm
from yukiho.utils.pagination import Pagination
from django.shortcuts import render, redirect, HttpResponse
from yukiho import models
from datetime import datetime
from yukiho.utils.pagination import Pagination
from django import forms
from django.core.validators import ValidationError
from yukiho.utils.form import DepartModelForm, LoginForm
from yukiho.utils.code import check_code
from io import BytesIO


def department_add(request):
    if request.method == "GET":
        form = DepartModelForm()
        content = {
            'form': form,
        }
        return render(request, 'department_add.html', content)
    form = DepartModelForm(data=request.POST)
    if form.is_valid():
        form.save()

        # return redirect('department/add')
        return redirect('/department/manage')
    return render(request, 'department_add.html', {'form': form})


def department_manage(request):
    search_data = request.GET.get('data', '')
    data_list = {}
    if search_data:
        data_list['depart__contains'] = search_data

    queryset = models.Department.objects.filter(**data_list)
    page_obj = Pagination(request, queryset)
    # return render(request, 'department_manage.html', {
    #
    #     'search_data': search_data,
    #
    #     'user_list': page_obj.page_queryset,
    #     'page_list_string': page_obj.show_page(),
    #
    # })
    content = {
        'search_data': search_data,
        'depart_list': page_obj.page_queryset,
        'page_list_string': page_obj.show_page(),
    }
    return render(request, 'department_manage.html', content)


def department_delete(request, uid):
    row_object = models.Department.objects.filter(id=uid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '未知数据'})
    row_object.delete()
    return redirect('/department/manage')


def department_edit(request, uid):
    row_object = models.Department.objects.filter(id=uid).first()
    if not row_object:
        return render(request, 'error.html', {'msg': '未知数据'})
    if request.method == 'GET':
        form = DepartModelForm(instance=row_object)
        return render(request, 'department_edit.html', {'form': form})

    form = DepartModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/department/manage')
    return render(request, 'department_edit.html', {'form': form})
