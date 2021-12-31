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


description = """
* 客户评分越高风险越低,评分范围:\t300~850, <br> **-9999**:\t表示无法评分或程序BUG
* 客户评级从**A**到**F**,\t**A**表示客户资信充分,可授信较高额度及较低费率,\t**F**表示客户资信不足,提高费率,谨慎授信
* 模型接口入参详情见:\t**Data**
"""


def create_app():
    app = FastAPI(title='风险评分评级模型',
                  description=description,
                  version='1.0')
    risk_router_init(app)
    return app
