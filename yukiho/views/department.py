from django.shortcuts import render, redirect, HttpResponse
from yukiho import models
from yukiho.utils.form import DepartModelForm
from yukiho.utils.pagination import Pagination


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
        return redirect('/department/add')
    return render(request, 'department_add.html', {'form': form})


def department_manage(request):
    search_data = request.GET.get('data', '')
    data_list = {}
    if search_data:
        data_list['depart__contains'] = search_data

    queryset = models.UserInfo.objects.filter(**data_list)
    page_obj = Pagination(request, queryset)
    return render(request, 'department_manage.html', {

        'search_data': search_data,

        'user_list': page_obj.page_queryset,
        'page_list_string': page_obj.show_page(),

    })
