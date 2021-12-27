# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 7:56 下午
# @Author  : HuangSir
# @FileName: load_dt.py
# @Software: PyCharm
# @Desc:

import json

def load_feature(file):
    with open(file, 'r') as f:
        data = f.read()
        data = data.split('\n')
        data = [i for i in data if i]
    return data

def load_json(file):
    with open(file,'r') as f:
        data = f.read()
        data = json.loads(data)
    return data

