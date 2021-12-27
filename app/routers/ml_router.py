# -*- coding: utf-8 -*-
# @Time    : 2021/11/6 11:35 下午
# @Author  : HuangSir
# @FileName: ml_router.py
# @Software: PyCharm
# @Desc: 模型路由

from fastapi import APIRouter
from app.app.applist_ml.core import AppData
from app.app.applist_ml.api import india_ml_main

from app.app.experian_ml.input_valid import InputData
from app.app.experian_ml.api import experian_report_credit_score

ml_router = APIRouter()


@ml_router.post('/v1/app/score', tags=['appList评分'])
async def app_score(data: AppData):
    data = data.dict()
    res = india_ml_main(data)
    return res


@ml_router.post('/v1/report/score', tags=['征信报告评分'])
async def report_score(data: InputData):
    data = data.dict()
    res = experian_report_credit_score(data)
    return res
