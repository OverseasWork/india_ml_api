# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 3:58 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc:

# from .lgbm_predict import experian_report_credit_score

from conf.log_config import log
from .lgbmcv_predict import experian_report_credit_score

def experian_main(reqId:str,reportJson: dict):
    if len(reportJson) == 0:
        log.logger.warning(f'{reqId}: experian is empty --------------------------------')
        return {'reqId': reqId, 'score':-9999,
                'code': 101, 'msg': '处理成功', 'detail':'输入为空', 'version': 'v1'}
    try:
        log.logger.info(f'{reqId}:starting experian --------------------------------')
        score = experian_report_credit_score(reqId,reportJson)
        log.logger.info(f'get experian score:{"%s"}' % score)
        return {'reqId': reqId, 'score': score,
                'code': 100, 'msg': '处理成功', 'version': 'v1'}
    except Exception as error:
        log.logger.error(f'{reqId},-----> {str(error)}')
        return {'reqId': reqId,
                'code': 102, 'msg': '处理失败', 'detail': str(error), 'version': 'v1'}