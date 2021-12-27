# -*- coding: utf-8 -*-
# @Time    : 2021/11/8 10:55 下午
# @Author  : HuangSir
# @FileName: data_model.py
# @Software: PyCharm
# @Desc: appList + adBook

from pydantic import BaseModel,Field
from typing import List


class AppList(BaseModel):
    """appList"""
    appName: str = Field(default=None, title='APP名称', example='Shazam',description='app名称')
    packageName: str = Field(title='包名', example='com.shazam.android',description='包名')
    firstInstallTime: int = Field(default=None, title='首次安装时间', example=1462084086000,description='首次安装时间戳')
    lastUpdateTime: int = Field(title='最近更新时间', example=1462084086000,description='最近更新时间戳')


class AppData(BaseModel):
    reqId: int = Field(title='请求编号,唯一标识符', example=134671)
    data: List[AppList] = Field(default=..., title='appList数据模型')
