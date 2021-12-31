# -*- coding: utf-8 -*-
# @Time    : 2021/12/30 11:50 上午
# @Author  : HuangSir
# @FileName: data_model.py
# @Software: PyCharm
# @Desc: 数据模型

from pydantic import BaseModel, Field
from typing import List

from app.app.applist_ml.core import AppList
from app.app.applist_ml.core import appListExample

from app.app.experian_ml.core import ExperianReport
from app.app.experian_ml.core import experianExample


class Data(BaseModel):
    """接口入参"""
    __doc__ = "模型接口入参"
    reqId: str = Field(title='请求编号', description='唯一标识符', example='2021039458294572')
    gender: int = Field(title='性别', description='枚举详情,男性:1,女性:0', example=1)
    age: int = Field(title='年龄', description='客户年龄', example=25)

    # ----------  通讯录信息 ------------------------
    concatNum: int = Field(title='通讯录有效个数', example=100, description='根据印度运营商号码组成规则对电话号码进行数据处理')

    concatApplyNum: int = Field(default=0, title='通讯录下单客户数', example=2, description='全平台手机号关联订单, 通讯录中下单客户数')

    concatApplyPassNum: int = Field(default=0, title='通讯录下单成功的客户数', example=1, description='全平台手机号关联订单, 通讯录中下单成功的客户数')

    concatApplyPassOdNum: int = Field(default=0, title='通讯录手机号关联订单数', example=0, description='通讯录手机号关联全平台订单数')

    concatApplyOverdueNum: int = Field(default=0, title='通讯录逾期客户数', example=0, description='通讯录手机号关联全平台逾期订单的手机号个数')

    concatApplyRatio: float = Field(default=0.0, title='通讯录申请占比', example=0.2, description='通讯录中全平台下单客户数*100/通讯录有效个数')

    concatRegisterRatio: float = Field(default=0.0, title='通讯录注册占比', example=0.1, description='通讯录中全平台注册客户数*100/通讯录有效个数')

    # appList+益博睿
    appList: List[AppList] = Field(default=..., title='appList详情', example=appListExample)
    experianReport: ExperianReport = Field(default=..., title='征信报告内容', example=experianExample)
