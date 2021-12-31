# -*- coding: utf-8 -*-
# @Time    : 2021/12/30 10:27 上午
# @Author  : HuangSir
# @FileName: risk_score.py
# @Software: PyCharm
# @Desc: 风险评分修正

from conf.log_config import log

from app.app.applist_ml.api import appList_main
from app.app.experian_ml.api import experian_main


def get_level(experian_score, appList_score):
    """获取客户等级"""
    if experian_score >= 600:  # 益博睿大于600
        if appList_score >= 600:
            level = 'A'
        elif appList_score > 0 and appList_score < 600:
            level = 'B'
        else:
            level = 'C'  # appList缺失
    elif experian_score > 0 and experian_score < 600:  # 益博睿大于 0 到 600
        if appList_score >= 600:
            level = 'B'
        elif appList_score > 0 and appList_score < 600:
            level = 'D'
        else:
            level = 'E'  # appList缺失
    else:  # # 益博睿缺失
        if appList_score >= 600:
            level = 'C'
        elif appList_score > 0 and appList_score < 600:
            level = 'E'
        else:
            level = 'F'  # appList缺失
    return level


def risk_score(data: dict):
    """主函数"""
    reqId = data['reqId']
    appList = data['appList']
    experian = data['experianReport']
    log.logger.info(f'{reqId}: starting run --------------------------------')
    appList_res = appList_main(reqId, appList)
    experian_res = experian_main(reqId, experian)

    detail = []
    if appList_res['code'] == 101:
        appList_score = -9999
    elif appList_res['code'] == 100:
        appList_score = appList_res['score']
    else:
        detail.append({'appList': appList_res['detail']})
        appList_score = -9998
    if experian_res['code'] == 101:
        experian_score = -9999
    elif experian_res['code'] == 100:
        experian_score = experian_res['score']
    else:
        detail.append({'experian': experian_res['detail']})
        experian_score = -9998

    # 客户等级
    level = get_level(appList_score=appList_score, experian_score=experian_score)

    age = data['age']
    gender = data['gender']
    zeros = [-9999, -9998]
    scoreL = [appList_score, experian_score]
    appList_experian_score = set(scoreL) - set(zeros)

    if appList_experian_score:
        score = max(appList_experian_score)

        # 年龄修正
        if age <= 24:
            score -= 8
            log.logger.info(f"age:{age}:-8")
        elif age > 24 and age <= 28:
            score -= 4
            log.logger.info(f"age:{age}:-4")
        elif age > 32 and age <= 36:
            score += 12
            log.logger.info(f"age:{age}:+3")
        elif age > 36:
            score += 6
            log.logger.info(f"age:{age}:+6")

        # 通讯录修复
        if data['concatApplyNum'] >= 10:
            score -= 3
            log.logger.info(f"concatApplyNum:{data['concatApplyNum']}:-3")

        if data['concatApplyNum'] == data['concatApplyPassNum'] and data['concatApplyNum'] > 1 and data['concatApplyNum'] < 10:
            score += 10
            log.logger.info(f"concatApplyNum:{data['concatApplyNum']},concatApplyNum:{data['concatApplyNum']}:10")

        if data['concatApplyPassOdNum'] == data['concatApplyOverdueNum'] and data['concatApplyPassOdNum'] != 0:
            score -= 10
            log.logger.info(f"concatApplyPassOdNum==concatApplyOverdueNum,{data['concatApplyOverdueNum']}:-10")

        if data['concatApplyRatio'] == data['concatApplyRatio'] and data['concatApplyNum'] >= 5:
            score -= 5
            log.logger.info(
                f"concatApplyRatio==concatApplyRatio:{data['concatApplyRatio']},concatApplyNum:{data['concatApplyNum']}:-5")

        if data['concatApplyOverdueNum'] == 0 and data['concatApplyPassOdNum'] >= 3:
            score += 15
            log.logger.info(f"concatApplyOverdueNum==0,concatApplyPassOdNum:{data['concatApplyPassOdNum']},+15")

        if data['concatNum'] >= 100 and data['concatNum'] <= 300:
            score += 5
            log.logger.info(f"concatNum:{data['concatNum']},+5")

        # 性别修正
        if gender == 0:
            score += 12
            log.logger.info(f"gender is Female,+12")
            # 等级修正
            if level not in ['A', 'B']:
                level = 'A'

        # 评分修正
        score = 850 if score > 850 else 300 if score < 300 else score

        # 等级修正
        log.logger.info(f"等级修正前:score:{score},level:{level}")
        if score >= 700 and level not in ['A','B','C']:
            level = 'C'
        elif score >= 600 and score < 700 and level not in ['B','C','D']:
            level = 'B' if level == 'A' else 'D'
        elif score > 0 and score < 600 and level not in ['C','D','E']:
            level = 'C' if level in ['A','B'] else 'E'
        log.logger.info(f"等级修正后:score:{score},level:{level}")

    else:
        log.logger.warning(f'{reqId}: none score result --------------------------------')
        score = -9999
        if gender == 1:
            level = 'E'
        else:
            level = 'B'

    if not detail:
        detail = 'success'

    result = {'reqId': reqId, 'score': score, 'level': level, 'details': detail}
    log.logger.info(f'{reqId}:finish predict,score:{score},level:{level} --------------------------------')
    return result
