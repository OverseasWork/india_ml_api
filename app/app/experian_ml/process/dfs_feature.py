# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 6:27 下午
# @Author  : HuangSir
# @FileName: dfs_feature.py
# @Software: PyCharm
# @Desc: 变量生成器

import featuretools as ft
import uuid

from .es_config import (
    report_summary_config,
    CAIS_Account_DETAILS_config,
    CAPS_Application_Details_config,
    CAIS_Account_History_config)

from pandas.core.base import DataError
import pandas as pd
import copy


def get_variable_types(es_config:dict):
    ''''''
    es_config_new = copy.deepcopy(es_config)
    variable_types = es_config_new['variable_types']
    # print(variable_types)
    res = {}
    for k,v in variable_types.items():
        if v == 'numeric':
            res[k] = ft.variable_types.Numeric
        elif v == 'ordinal':
            res[k] = ft.variable_types.Ordinal
        elif v == 'date_of_birth':
            res[k] = ft.variable_types.DateOfBirth
        elif v == 'datetime':
            res[k] = ft.variable_types.Datetime
        elif v == 'categorical':
            res[k] = ft.variable_types.Categorical
        elif v == 'phone_number':
            res[k] = ft.variable_types.PhoneNumber
        else:
            res[k] = ft.variable_types.Numeric
    es_config_new['variable_types'] = res
    return es_config_new

def df_to_ftset(report):
    es = ft.EntitySet(id=str(uuid.uuid1()))
    config = get_variable_types(report_summary_config)
# try:
#     es = es.entity_from_dataframe(dataframe=report_summary_df, **report_summary_config)
# except (TypeError,LookupError):
#     del report_summary_config['variable_types']
    es = es.entity_from_dataframe(dataframe=report.report_summary, **config)

    config = get_variable_types(CAIS_Account_DETAILS_config)
    # try:
    #     es = es.entity_from_dataframe(dataframe=CAIS_Account_DETAILS_df, **CAIS_Account_DETAILS_config)
    # except (TypeError,LookupError):
    #     del CAIS_Account_DETAILS_config['variable_types']
    es = es.entity_from_dataframe(dataframe=report.CAIS_Account_DETAILS,**config)

    config = get_variable_types(CAPS_Application_Details_config)
# try:
#     es = es.entity_from_dataframe(dataframe=CAPS_Application_Details_df, **CAPS_Application_Details_config)
# except (TypeError,LookupError):
#     del CAPS_Application_Details_config['variable_types']
    es = es.entity_from_dataframe(dataframe=report.CAPS_Application_Details, **config)

    config = get_variable_types(CAIS_Account_History_config)
# try:
#     es = es.entity_from_dataframe(dataframe=CAIS_Account_History_df, **CAIS_Account_History_config)
# except (TypeError,LookupError):
#     del CAIS_Account_History_config['variable_types']
#     print(report.CAIS_Account_History.fillna(-9999))
    es = es.entity_from_dataframe(dataframe=report.CAIS_Account_History, **config)

    rl1 = ft.Relationship(es['summary']['loan_app_id'], es['CAIS_Account']['loan_app_id'])
    rl2 = ft.Relationship(es['summary']['loan_app_id'], es['CAPS_Application']['loan_app_id'])
    rl3 = ft.Relationship(es['summary']['loan_app_id'], es['CAIS_Account_History']['loan_app_id'])
    es = es.add_relationship(rl1)
    es = es.add_relationship(rl2)
    es = es.add_relationship(rl3)
    return es

def get_feature_matrix(features:list,es,cat_factorize:dict):
# try:
    matrix_data = ft.calculate_feature_matrix(features = features,entityset=es,n_jobs=1)
# except (DataError,TypeError,AssertionError,ValueError,KeyError):
#     matrix_data = pd.DataFrame([{**{k.get_name() : -9999 for k in features},'reqId':'未知'}]
#                                ).set_index(keys='reqId')

    matrix_data = matrix_data.fillna(-9999)
    matrix_data[list(cat_factorize.keys())] = matrix_data[list(cat_factorize.keys())].astype('str')
    matrix_data = matrix_data.replace(cat_factorize)
    matrix_data[matrix_data.select_dtypes(include='object').columns] =\
        matrix_data[matrix_data.select_dtypes(include='object').columns].astype('float')
    return matrix_data