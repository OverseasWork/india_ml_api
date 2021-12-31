# -*- coding: utf-8 -*-
# @Time    : 2021/12/19 6:49 下午
# @Author  : HuangSir
# @FileName: api.py
# @Software: PyCharm
# @Desc: 模型主程序

from conf.log_config import log

from app.app.applist_ml.applist_model import AppListML

appModel = AppListML()


def appList_main(reqId:str,appListData:list):
    """appList主函数"""
    if len(appListData) == 0:
        log.logger.warning(f'{reqId}: appList is empty --------------------------------')
        return {'reqId': reqId, 'prob':-9999, 'score':-9999,
                'code': 101, 'msg': '处理成功', 'detail':'输入为空', 'version': 'v1'}
    try:
        log.logger.info(f'{reqId}:starting appList --------------------------------')
        app_res = appModel.applist_ml_predict(reqId,appListData)
        log.logger.info(f"get appModel prob:{app_res['prob']},score:{app_res['score']}")
        return {'reqId': reqId, 'prob': app_res['prob'], 'score': app_res['score'],
                'code': 100, 'msg': '处理成功', 'version': 'v1'}
    except Exception as error:
        log.logger.error(f'{reqId},-----> {str(error)}')
        return {'reqId': reqId, 'code': 102, 'msg': '处理失败', 'detail': str(error), 'version': 'v1'}
