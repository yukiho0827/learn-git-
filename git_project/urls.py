"""git_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from yukiho.views import department, user, account, admin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('department/add', department.department_add),
    path('department/<int:uid>/delete', department.department_delete),
    path('department/<int:uid>/edit', department.department_edit),
    path('department/manage', department.department_manage),
    path('admin/add', admin.admin_add),
    path('admin/manage', admin.admin_manage),
    path('admin/<int:uid>/delete', admin.admin_delete),
    path('admin/<int:uid>/edit', admin.admin_edit),
    path('user/add', user.user_add),
    path('user/<int:uid>/delete', user.user_delete),
    path('user/<int:uid>/edit', user.user_edit),
    path('user/manage', user.user_manage),
    path('login', account.login),
    path('logout', account.logout),
    path('image/code', account.image_code),

]
