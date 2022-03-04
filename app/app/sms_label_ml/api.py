# -*- coding: utf-8 -*-
# @Time    : 2022/3/4 11:43 上午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc: 短信模型分

from conf.log_config import log
from typing import List
from app.app.sms_label_ml.sms_card import SmsCardModel

smsMl = SmsCardModel()


def smsList_main(reqId:str,smsList:List[dict]):
    """smsList主函数"""
    if len(smsList) == 0:
        log.logger.warning(f'{reqId}: smsList is empty --------------------------------')
        return {'reqId': reqId, 'prob':-9999, 'score':-9999,
                'code': 101, 'msg': '处理成功', 'detail':'输入为空', 'version': 'v1'}
    # try:
    log.logger.info(f'{reqId}:starting smsList --------------------------------')
    score = smsMl.predict(smsList)
    log.logger.info(f"get smsModel score:{score}")
    return {'reqId': reqId, 'score': score,
            'code': 100, 'msg': '处理成功', 'version': 'v1'}
    # except Exception as error:
    #     log.logger.error(f'{reqId},-----> {str(error)}')
    #     return {'reqId': reqId, 'code': 102, 'msg': '处理失败', 'detail': str(error), 'version': 'v1'}

