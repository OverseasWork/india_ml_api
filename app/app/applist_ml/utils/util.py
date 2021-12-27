import pandas as pd
import  datetime
import time
import joblib
import numpy as np
import sys
sys.path.append('..')


def loan_dt(url):
    dt = pd.read_json(url)
    dt = dt.to_dict(orient='index')
    res = [i for i in dt.values()]
    return res


def stamp_format(tm):
    te=time.strftime("%Y-%m-%d", time.localtime(int(str(tm)[:10])))
    if te>datetime.datetime.strftime(datetime.datetime.today(),'%Y-%m-%d') or te<'2000-1-1':
        return '1990-1-1'
    else:
        return te


def load_model(path):
    lgb = joblib.load(path)
    return lgb


def prob2Score(prob,basePoint=600,PDO=100,odds=30):
    # 将违约概率转化成分数
    y = np.log(prob/(1-prob))
    a = basePoint - y * np.log(odds)
    y2 = a - PDO/np.log(2)*(y)
    score = y2.astype('int')
    return score


def load_txt_feat(file: str):
    """加载txt"""
    with open(file, 'r') as f:
        feature = f.read().split('\n')
        feature = [i for i in feature if i]
        return feature
