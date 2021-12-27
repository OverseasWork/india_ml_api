# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 1:53 下午
# @Author  : HuangSir
# @FileName: input_valid.py
# @Software: PyCharm
# @Desc:

from pydantic import BaseModel, Field


class INProfileResponse(BaseModel):
    SCORE = ''
    TotalCAPS_Summary = ''
    NonCreditCAP = ''
    NonCreditCAPS_Summary = ''
    CAIS_Account = ''
    CAIS_Summary = ''
    Total_Outstanding_Balance = ''
    Credit_Account = ''
    CAPS = ''
    CAPS_Summary = ''
    CAIS_Account_DETAILS = ''
    CAPS_Application_Details = ''


class ReportJson(BaseModel):
    """数据报告"""
    # INProfileResponse: dict
    inProfileResponse: INProfileResponse = ...


class InputData(BaseModel):
    reqId: str = Field(title='请求编号,唯一标识符', example='134671')
    reportJson: ReportJson = ...

