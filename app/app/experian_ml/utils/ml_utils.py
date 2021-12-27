# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 8:06 下午
# @Author  : HuangSir
# @FileName: ml_utils.py
# @Software: PyCharm
# @Desc:

import numpy as np


def prob2Score(prob, basePoint=600, PDO=100, odds=30):
    y = np.log(prob / (1 - prob))
    a = basePoint - y * np.log(odds)
    y2 = a - PDO / np.log(2) * (y)
    score = y2.astype('int')
    return score
