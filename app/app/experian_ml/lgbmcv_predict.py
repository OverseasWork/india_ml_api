# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 8:07 下午
# @Author  : HuangSir
# @FileName: lgbmcv_predict.py
# @Software: PyCharm
# @Desc:

import numpy as np
import pandas as pd
import uuid

from .load_file import (dfsFeatures,
                        cat_factorize,
                        features,
                        cat_features,
                        lgbmCV)

from .process import (Report,
                     df_to_ftset,
                     get_feature_matrix)

from .utils.ml_utils import prob2Score


def get_ml_data(reqId:str, reportJson:dict):
    report = Report(reqId=reqId,reportJson=reportJson)
    es = df_to_ftset(report)
    ml_data = get_feature_matrix(es=es,features=dfsFeatures,cat_factorize=cat_factorize)
    return ml_data


def experian_report_credit_score(reqId:str,reportJson: dict):
    ml_data = get_ml_data(reqId,reportJson)
    zeros = (-999,)
    if set(ml_data[features].values.tolist()[0]) == set(zeros):
        return -9999

    l_cv = len(lgbmCV)
    prob = np.mean([lgbmCV[i].predict(ml_data[features]) for i in range(l_cv)], axis=0)
    score = prob2Score(prob)
    # ml_data = ml_data.to_dict(orient='index')[data['reqId']]
    # ml_data = {k: v if isinstance(v, bool) else int(v) if isinstance(v, int) else float(v)
    #            for k, v in ml_data.items()}
    return score
