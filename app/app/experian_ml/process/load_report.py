# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 4:57 下午
# @Author  : HuangSir
# @FileName: load_report.py
# @Software: PyCharm
# @Desc: 获取报告详情

import pandas as pd
import numpy as np
from datetime import datetime
import copy

from .es_config import (
    report_summary_config,
    CAIS_Account_DETAILS_config,
    CAPS_Application_Details_config,
    CAIS_Account_History_config)


def str2num(x):
    x_new = copy.deepcopy(x)
    x_new = str(x_new)
    if '.' in x_new:
        try:
            return float(x_new)
        except:
            return np.nan
    else:
        try:
            return int(float(x_new))
        except:
            return np.nan


class Report(object):
    def __init__(self, reqId: str, reportJson: dict):
        self.reqId = reqId
        self.reportJson = reportJson.get('INProfileResponse', {})
        self.report_summary = self.__report_summary()
        self.CAIS_Account_DETAILS = self.__CAIS_Account_DETAILS()
        self.CAPS_Application_Details = self.__CAPS_Application_Details()
        self.CAIS_Account_History = self.__CAIS_Account_History()

    def __drop_cols_func(self, dt: [dict, pd.DataFrame], cols: list):
        for col in cols:
            try:
                del dt[col]
            except KeyError:
                pass
        return dt

    def __to_df(self,res: pd.DataFrame, drop_cols: list):
        res = self.__drop_cols_func(res, drop_cols)
        res.replace({'': np.nan}, inplace=True)
        return res

    def __formatdate(self,datestr: str):
        try:
            if int(float(datestr[:4])) > 2020 or int(float(datestr[:4])) < 2000:
                fdate = np.nan
            else:
                try:
                    fdate = datetime.strptime(datestr, '%Y%m%d').strftime('%Y-%m-%d')
                except:
                    fdate = np.nan
        except:
            fdate = np.nan
        return fdate

    def __trans_types(self,df,config):
        '''类型转换'''
        config_new = copy.deepcopy(config)
        type_string = config_new['variable_types']
        for k, v in type_string.items():
            if k not in df.columns:
                # print(k)
                df[k] = np.nan
            if v == 'numeric':
                df[k] = df[k].apply(lambda x: str2num(x))
        return df

    def __report_summary(self):
        SCORE = self.reportJson.get('SCORE', {})
        TotalCAPS_Summary = self.reportJson.get('TotalCAPS_Summary', {})
        NonCreditCAPS_Summary = self.reportJson.get('NonCreditCAPS', {}).get('NonCreditCAPS_Summary', {})
        Total_Outstanding_Balance = self.reportJson.get('CAIS_Account', {}).get('CAIS_Summary', {}).get(
            'Total_Outstanding_Balance', {})
        Credit_Account = self.reportJson.get('CAIS_Account', {}).get('CAIS_Summary', {}).get('Credit_Account', {})
        CAPS_Summary = self.reportJson.get('CAPS', {}).get('CAPS_Summary', {})
        res = {**SCORE, **TotalCAPS_Summary, **NonCreditCAPS_Summary, **Total_Outstanding_Balance, **Credit_Account,
               **CAPS_Summary}
        drop_cols = ['CreditRating']
        res = pd.DataFrame([res])
        res = self.__to_df(res, drop_cols)
        res['loan_app_id'] = self.reqId
        res = self.__trans_types(res,report_summary_config)
        return res

    def __CAIS_Account_DETAILS(self):
        CAIS_drop_key = ['CAIS_Holder_Details', 'CAIS_Account_History', 'CAIS_Holder_Address_Details',
                         'CAIS_Holder_Phone_Details', 'CAIS_Holder_ID_Details']

        CAIS_d = self.reportJson.get('CAIS_Account', {}).get('CAIS_Account_DETAILS', [])
        if isinstance(CAIS_d, dict):
            CAIS_d = [CAIS_d]
        CAIS_d = [{k: v for k, v in item.items() if k not in CAIS_drop_key} for item in CAIS_d]

        drop_cols = ['Identification_Number', 'LitigationStatusDate', 'Original_Charge_off_Amount',
                     'SuitFiledWillfulDefaultWrittenOffStatus',
                     'Value_of_Credits_Last_Month', 'Subscriber_comments', 'CurrencyCode',
                     'Scheduled_Monthly_Payment_Amount',
                     'Payment_History_Profile', 'Account_Number', 'Special_Comment', 'DefaultStatusDate',
                     'Income_Indicator', 'Type_of_Collateral',
                     'Date_Of_First_Delinquency', 'WriteOffStatusDate', 'Income_Frequency_Indicator',
                     'Consumer_comments', 'Promotional_Rate_Flag',
                     'Income', 'Value_of_Collateral', 'Occupation_Code', 'SuitFiled_WilfulDefault',
                     'Written_off_Settled_Status',
                     'Credit_Limit_Amount']
        res = pd.DataFrame(CAIS_d)
        res = self.__to_df(res, drop_cols)
        for col in ['Open_Date', 'DateOfAddition',
                    'Date_Reported', 'Date_Closed', 'Date_of_Last_Payment']:
            try:
                res[col] = res[col].apply(lambda x:self. __formatdate(str(x)))
            except KeyError:
                res[col] = np.nan

        res['loan_app_id'] = self.reqId
        res = self.__trans_types(res,CAIS_Account_DETAILS_config)
        # print(res.info())
        return res

    def __CAPS_Application_Details(self):
        CAPS_drop_key = ['CAPS_Applicant_Details', 'CAPS_Applicant_Address_Details', 'CAPS_Other_Details',
                         'CAPS_Applicant_Additional_Address_Details']

        CAPS_d = self.reportJson.get('CAPS', {}).get('CAPS_Application_Details', [])
        if isinstance(CAPS_d, dict):
            CAPS_d = [CAPS_d]
        CAPS_d = [{
            **{k: v for k, v in item.items() if k not in CAPS_drop_key},
            **item.get('CAPS_Applicant_Details', {}),
            **item.get('CAPS_Other_Details', {})
        } for item in CAPS_d
        ]
        drop_cols = ['Employment_Status', 'Time_with_Employer', 'Number_of_Major_Credit_Card_Held', 'Income',
                     'ReportTime', 'IncomeTaxPan',
                     'PAN_Issue_Date', 'Passport_number', 'Voter_ID_Expiration_Date', 'Telephone_Number_Applicant_1st',
                     'Voter_s_Identity_Card',
                     'Middle_Name2', 'Middle_Name1', 'Middle_Name3', 'First_Name', 'Ration_Card_Issue_Date',
                     'Telephone_Extension', 'Driver_License_Number',
                     'Voter_ID_Issue_Date', 'PAN_Expiration_Date', 'Universal_ID_Number',
                     'Universal_ID_Expiration_Date',
                     'Ration_Card_Number', 'Driver_License_Expiration_Date', 'EMailId', 'Universal_ID_Issue_Date',
                     'Ration_Card_Expiration_Date',
                     'Last_Name', 'Driver_License_Issue_Date', 'Passport_Expiration_Date', 'Passport_Issue_Date',
                     'Subscriber_code',
                     'ReportNumber', 'Marital_Status']

        res = pd.DataFrame(CAPS_d)
        res = self.__to_df(res, drop_cols)
        for col in ['Date_of_Request', 'Date_Of_Birth_Applicant']:
            try:
                res[col] = res[col].apply(lambda x: self.__formatdate(str(x)))
            except KeyError:
                res[col] = np.nan
        res['loan_app_id'] = self.reqId
        res = self.__trans_types(res,CAPS_Application_Details_config)
        return res

    def __CAIS_Account_History(self):
        CAIS_Account_DETAILS = self.reportJson.get('CAIS_Account', {}).get('CAIS_Account_DETAILS', [])
        if isinstance(CAIS_Account_DETAILS, dict):
            CAIS_Account_DETAILS = [CAIS_Account_DETAILS]
        res = []
        for i, de in enumerate(CAIS_Account_DETAILS):
            d = de.get('CAIS_Account_History', [])
            if isinstance(d, dict):
                d = [d]
            res += d
        res = pd.DataFrame(res)
        res['loan_app_id'] = self.reqId
        res = self.__to_df(res,[])
        res = self.__trans_types(res,CAIS_Account_History_config)
        return res