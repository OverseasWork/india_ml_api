# -*- coding: utf-8 -*-
# @Time    : 2020/10/29 8:49 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc:

import warnings
warnings.filterwarnings('ignore')

from .routers import risk_router_init
from fastapi import FastAPI


def create_app():
    app = FastAPI(title='AppList评分模型',
                  description='基于appList风险评分模型,\n'
                              ' 入参详情见 ** AppData',
                  version='1.0')
    risk_router_init(app)
    return app
