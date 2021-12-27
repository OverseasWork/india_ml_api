# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 8:07 下午
# @Author  : HuangSir
# @FileName: lgbm_predict.py
# @Software: PyCharm
# @Desc:


from .load_file import (dfsFeatures,
                        cat_factorize,
                        features,
                        cat_features,
                        lgbm)
from .process import (CreditReport,
                     df_to_ftset,
                     get_feature_matrix)

from .input_valid import InputData
from pydantic import ValidationError

import lightgbm as lgb

from .utils.ml_utils import prob2Score

def get_ml_data(data:dict):
    report_obj = CreditReport(reqId=data['reqId'],reportJson=data['reportJson'])
    es = df_to_ftset(report_obj)
    ml_data = get_feature_matrix(es=es,features=dfsFeatures,cat_factorize=cat_factorize)
    return ml_data


def experian_report_credit_score(data:dict):
    try:
        data = InputData(**data).dict()
    except ValidationError as err:
        return {'msg': '入参错误', 'detail': str(err)}
    ml_data = get_ml_data(data)
    prob = lgbm.predict(ml_data)[0]
    score = prob2Score(prob)
    ml_data = ml_data.to_dict(orient='index')[data['reqId']]
    ml_data = {k: v if isinstance(v,bool) else int(v) if isinstance(v, int) else float(v)
               for k, v in ml_data.items()}
    res = {'reqId': data['reqId'], 'prob': float(prob), 'score': int(score), 'data': ml_data}
    return res
