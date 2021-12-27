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

from .input_valid import InputData
from pydantic import ValidationError

from .utils.ml_utils import prob2Score


def get_ml_data(data: dict):
    report = Report(reqId=data['reqId'],reportJson=data['reportJson'])
    es = df_to_ftset(report)
    ml_data = get_feature_matrix(es=es,features=dfsFeatures,cat_factorize=cat_factorize)
    # debug ----------------------------------
    # ml_data = ml_data.to_dict(orient='index')[data['reqId']]
    # ml_data['MEAN(CAPS_Application.Amount_Financed)'] = 235153.8846153847
    # ml_data['MEDIAN(CAIS_Account.AGE(Open_Date))'] = 0.8630136986301371
    # ml_data['MIN(CAIS_Account.AGE(Open_Date))'] = 0.2191780821917808
    # ml_data = pd.DataFrame([ml_data],index=[data['reqId']])
    # debug ----------------------------------
    return ml_data


def experian_report_credit_score(data: dict):
    try:
        data = InputData(**data).dict()
    except ValidationError as err:
        return {'msg': 'error', 'detail': str(err)}

    ml_data = get_ml_data(data)
    l_cv = len(lgbmCV)
    prob = np.mean([lgbmCV[i].predict(ml_data[features]) for i in range(l_cv)], axis=0)
    score = prob2Score(prob)
    # try:
    ml_data = ml_data.to_dict(orient='index')[data['reqId']]
    # except KeyError:
    #     ml_data = ml_data.to_dict(orient='index')['未知']
    ml_data = {k: v if isinstance(v, bool) else int(v) if isinstance(v, int) else float(v)
               for k, v in ml_data.items()}
    res = {'reqId': data['reqId'], 'prob': float(prob), 'score': int(score), 'data': ml_data, 'msg': 'success'}
    return res
