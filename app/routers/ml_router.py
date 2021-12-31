# -*- coding: utf-8 -*-
# @Time    : 2021/11/6 11:35 下午
# @Author  : HuangSir
# @FileName: ml_router.py
# @Software: PyCharm
# @Desc: 模型路由

from fastapi import APIRouter

from app.app.api import risk_main
from app.app.data_model import Data

ml_router = APIRouter()

@ml_router.post('/v1/app/risk_score',tags=['风险评分评级'])
async def risk_score(data:Data):
    data = data.dict()
    res = risk_main(data)
    return res
