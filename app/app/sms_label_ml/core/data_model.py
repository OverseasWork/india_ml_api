# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 3:01 下午
# @Author  : HuangSir
# @FileName: data_model.py
# @Software: PyCharm
# @Desc:

from pydantic import BaseModel,Field

class SmsList(BaseModel):
    """smsList"""
    otherName: str = Field(title='姓名',description='对方姓名')
    otherMobile: str = Field(title='电话',description='对方号码')
    type: int = Field(title='类型',description='短信类型,1:接收, 2:发送')
    messageContent: str = Field(title='内容',description='短信内容')
    messageTime: int = Field(title='时间戳',description='短信接收时间')