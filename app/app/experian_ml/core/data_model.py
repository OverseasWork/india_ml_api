# -*- coding: utf-8 -*-
# @Time    : 2021/12/27 6:23 下午
# @Author  : HuangSir
# @FileName: data_model.py
# @Software: PyCharm
# @Desc: 数据模型

from pydantic import BaseModel,Field
from typing import List

class ExperianReport(BaseModel):
    SCORE:dict = {}
    TotalCAPS_Summary:dict = {}
    NonCreditCAPS:dict = {}
    CAIS_Account:dict = {}
    CAPS:dict = {}