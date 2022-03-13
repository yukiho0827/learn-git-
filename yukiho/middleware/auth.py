#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 后续还加
        if request.path_into in ['/login']:
            return
        info_dict = request.session.get('info')
        if not info_dict:
            return redirect('/login')
        return

    def process_response(self, request, response):

        return response
