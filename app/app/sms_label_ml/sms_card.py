# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 3:18 下午
# @Author  : HuangSir
# @FileName: sms_model.py
# @Software: PyCharm
# @Desc: 短信评分模型

from conf.log_config import log

import sys
sys.path.append('..')
from typing import List
from collections import Counter
import pandas as pd
from utils import scorecard_ply
from app.app.sms_label_ml.sms_label import sms_ml_label

class SmsCardModel:
    def __init__(self):
        self.file = 'app/app/sms_label_ml/static/'
        self.card = pd.read_excel(self.file+'card_df.xlsx')
        # 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        self.tL = [chr(i) for i in range(ord('A'),ord('P')+1)]

    def __card_feat(self,smsList:List[dict]):
        sms_labels = sms_ml_label(smsList)
        if sms_labels:
            total_cnt = len(sms_labels)
            featD = dict(Counter(sms_labels))
            featD = {f'label{i}':featD.get(f'label{i}',0) for i in self.tL}
            featD = {'total_cnt':total_cnt,**featD}
            res = featD
            return res
        else:
            return {}

    def __tmp_card(self,smsList:List[dict]):
        # log.logger.info('get smsList score.........................................')
        s = 600
        featS = self.__card_feat(smsList)
        if featS:
            # total_cnt
            if featS['total_cnt'] <= 50:
                s -= 100
            elif featS['total_cnt'] >= 50 and featS['total_cnt'] <= 500:
                s += 50
            else:
                s += 20
            # log.logger.info(f"total_cnt: {featS['total_cnt']},score:{s}")

            # labelC 申请通过
            if featS['labelC'] > 0 and featS['labelC'] <= 5:
                s += 5
            elif featS['labelC'] > 5 and featS['labelC'] <= 9:
                s += 10
            elif featS['labelC'] > 9:
                s += 15
            # log.logger.info(f"labelC: {featS['labelC']},score:{s}")

            # labelD 放款成功
            if featS['labelD'] > 0 and  featS['labelD'] <= 3:
                s += 10
            elif featS['labelD'] > 3 and featS['labelD'] <= 6:
                s += 30
            elif featS['labelD'] > 6 and featS['labelD'] <= 10:
                s += 50
            elif featS['labelD'] > 10:
                s += 70
            # log.logger.info(f"labelD: {featS['labelD']},score:{s}")

            # labelF 还款成功
            if featS['labelF'] > 0 and  featS['labelF'] <= 3:
                s += 10
            elif featS['labelF'] > 3 and featS['labelF'] <= 6:
                s += 30
            elif featS['labelF'] > 6 and featS['labelF'] <= 10:
                s += 50
            elif featS['labelF'] > 10:
                s += 80
            # log.logger.info(f"labelF: {featS['labelF']},score:{s}")

            # labelB 申请拒绝
            if featS['labelB'] == 0:
                s += 5
            elif featS['labelB'] > 0 and  featS['labelB'] <= 5:
                s -= 5
            elif featS['labelB'] > 5 and featS['labelB'] <= 10:
                s -= 10
            elif featS['labelB'] > 10 and featS['labelB'] <= 20:
                s -= 20
            elif featS['labelB'] > 20:
                s -= 40
            # log.logger.info(f"labelB: {featS['labelB']},score:{s}")

            # labelG 逾期催收
            if featS['labelG'] == 0:
                s += 5
            elif featS['labelG'] > 0 and  featS['labelG'] <= 5:
                s -= 15
            elif featS['labelG'] > 5 and featS['labelG'] <= 10:
                s -= 25
            elif featS['labelG'] > 10 and featS['labelG'] <= 20:
                s -= 35
            elif featS['labelG'] > 20:
                s -= 90
            # log.logger.info(f"labelG: {featS['labelG']},score:{s}")

            # labelJ 重度逾期
            if featS['labelJ'] == 0:
                s += 5
            elif featS['labelJ'] > 0 and  featS['labelJ'] <= 5:
                s -= 15
            elif featS['labelJ'] > 5 and featS['labelJ'] <= 10:
                s -= 45
            elif featS['labelJ'] > 10 and featS['labelJ'] <= 20:
                s -= 60
            elif featS['labelJ'] > 20:
                s -= 100
            # log.logger.info(f"labelJ: {featS['labelJ']},score:{s}")

            # labelP 额度提升
            if featS['labelP'] > 0 and featS['labelP'] <= 3:
                s += 5
            elif featS['labelP'] > 3 and featS['labelP'] <= 6:
                s += 7
            elif featS['labelP'] > 6 and featS['labelP'] <= 10:
                s += 9
            elif featS['labelP'] > 10:
                s += 28
            # log.logger.info(f"labelP: {featS['labelP']},score:{s}")

        return s

    def predict(self,smsList:List[dict]):
        score = self.__tmp_card(smsList)
        return score

    # def predict(self, data: dict):
    #     # 变量置换
    #     ml_data = {v:[data[k]] for k,v in FeatMap.items()}
    #     # 数据格式构造
    #     # print(ml_data)
    #     ml_df = pd.DataFrame(ml_data)
    #     # 预测
    #     score_result = scorecard_ply(dt=ml_df,card=self.lr_card,only_total_score=False)
    #     score_result = score_result.to_dict(orient='index')[0]
    #     return score_result