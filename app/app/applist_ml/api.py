# -*- coding: utf-8 -*-
# @Time    : 2021/12/19 6:49 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc: 模型主程序

from conf.log_config import log

from app.app.applist_ml.applist_model import AppListML

appModel = AppListML()


def india_ml_main(data):

    reqId = data['reqId']
    ml_data = data
    if len(data['data']) == 0:
        log.logger.warning(f'{reqId}: appList is empty --------------------------------')
        return {'reqId': reqId, 'prob':-9999, 'score':-9999,
                'code': 101, 'msg': '处理成功', 'detail':'输入为空', 'version': 'v1'}
    try:
        log.logger.info(f'{reqId}:starting appList --------------------------------')
        prob = appModel.applist_ml_predict(ml_data)
        ml_data['prob'] = prob
        log.logger.info(f'get appModel prob:{"%s"}' % prob['prob'])

        return {'reqId': reqId, 'prob': prob['prob'], 'score': prob['score'],
                'code': 100, 'msg': '处理成功', 'version': 'v1'}
    except Exception as error:
        log.logger.error(f'{reqId},-----> {str(error)}')
        return {'reqId': reqId, 'code': 102, 'msg': '处理失败', 'detail': str(error), 'version': 'v1'}
