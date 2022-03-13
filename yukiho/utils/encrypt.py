"""
md5加密
"""

import hashlib
from django.conf import settings


def md5(data):
    # 加盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    # 更新
    obj.update(data.encode('utf-8'))
    # 返回
    return obj.hexdigest()
