# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 11:30 上午
# @Author  : HuangSir
# @FileName: sms_label.py
# @Software: PyCharm
# @Desc: 短信标签

import pandas as pd
import os
import string
import joblib
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from keras.models import load_model
from typing import List
import re
import sys
sys.path.append('..')
sys.path.append(os.getcwd())


file_path = 'app/app/sms_label_ml/data/'

TOKEN_DIR=file_path+'tokenizer_V2.pkl'
KERAS_DIR=file_path+'word_vector_cnn_V2.h5'

tokenizer=joblib.load(TOKEN_DIR)
keras_model=load_model(KERAS_DIR)

MAX_SEQUENCE_LENGTH = 100

def str_opr(data,text_col):
    data[text_col] = data[text_col].apply(lambda x:str(x).lower())
    data[text_col]= data[text_col].apply(lambda x: ' '.join(x for x in x.split(' ') if x not in string.punctuation))
    data[text_col]= data[text_col].str.replace('[^\w\s]','')
    data[text_col]= data[text_col].apply(lambda x: ' '.join(x for x in x.split(' ') if not x.isdigit()))
    data[text_col]= data[text_col].str.replace('\d+','')
    return data[text_col]


def predict_label(test_sentence):
    sequences = tokenizer.texts_to_sequences([test_sentence.split(' ')])
    test_text = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
    y_pred_class=np.argmax(keras_model.predict(test_text), axis=1)
    maps={0: 'labelA',
             1: 'labelB',
             2: 'labelC',
             3: 'labelD',
             4: 'labelE',
             5: 'labelF',
             6: 'labelH',
             7: 'labelI',
             8: 'labelJ',
             9: 'labelK',
             10: 'labelL',
             11: 'labelM',
             12: 'labelP'}
    pred=maps[y_pred_class[0]]
    return pred

# def loan_dt(url)->List[dict]:
#     '''下载短信数据'''
#     try:
#         jsdt = pd.read_json(url)
#     except:
#         jsdt = pd.DataFrame([])
#     jsdt = jsdt.to_dict(orient='index')
#     res = [i for i in jsdt.values()]
#     return res

def filter_org(smsList: List[dict]) -> List[dict]:
    '''发送短信'''
    try:
        res = [s for s in smsList if \
               s['type'] == 1 and \
               s['otherName'] == s['otherMobile'] and \
               bool(re.search('[a-zA-Z]', str(s['otherMobile'])))
               ]
    except KeyError as err:
        print(f'{str(err)},{smsList}')
        res = []
    return res

def sms_ml_label(smsList:List[dict]):
    smsList = filter_org(smsList)
    data = pd.DataFrame(smsList)
    if data.empty:
        return []
    else:
        data.rename(columns={'otherMobile': 'sender', 'messageContent': 'text', 'messageTime': 'date'}, inplace=True)
        data['text'] = str_opr(data, 'text')
        data['label'] = data['text'].apply(predict_label)
        result = data['label'].tolist()
        return result

