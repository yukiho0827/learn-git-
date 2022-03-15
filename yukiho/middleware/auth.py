#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 后续还加
        print(1)
        if request.path_info in ['/login', '/image/code']:
            print(2)
            return
        print(3)
        info_dict = request.session.get('info')
        print(4)
        if not info_dict:
            return redirect('/login')
        return

    def process_response(self, request, response):

        return response
