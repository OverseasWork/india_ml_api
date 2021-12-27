# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 8:10 下午
# @Author  : HuangSir
# @FileName: load_file.py
# @Software: PyCharm
# @Desc: 加载文件

import sys
sys.path.append('..')

path = 'app/app/experian_ml/data/'
# path = 'output/'

import featuretools as ft
import lightgbm as lgb
import joblib
from .utils.load_dt import load_json,load_feature

dfsFeatures = ft.load_features(f'{path}dfs_features.json')

cat_factorize = load_json(f'{path}cat_factorize.json')

features = load_feature(f'{path}features.txt')

cat_features = load_feature(f'{path}cat_features.txt')

num_features = load_feature(f'{path}num_features.txt')

# --------load model --------------------

lgbm = lgb.Booster(model_file=f'{path}exp_report_ml')
lgbmCV = joblib.load(f'{path}exp_report_ml_cv.pkl')
