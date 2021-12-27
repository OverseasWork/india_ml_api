# -*- coding: utf-8 -*-
# @Time    : 2020/12/30 6:45 下午
# @Author  : HuangSir
# @FileName: es_config.py
# @Software: PyCharm
# @Desc:

report_summary_config = {
    'entity_id': 'summary',
    'index': 'loan_app_id',
    'variable_types': {'BureauScore': 'numeric',
                       'BureauScoreConfidLevel': 'ordinal',
                       'CADSuitFiledCurrentBalance': 'numeric',
                       'CAPSLast180Days': 'numeric',
                       'CAPSLast30Days': 'numeric',
                       'CAPSLast7Days': 'numeric',
                       'CAPSLast90Days': 'numeric',
                       'CreditAccountActive': 'numeric',
                       'CreditAccountClosed': 'numeric',
                       'CreditAccountDefault': 'numeric',
                       'CreditAccountTotal': 'numeric',
                       'NonCreditCAPSLast180Days': 'numeric',
                       'NonCreditCAPSLast30Days': 'numeric',
                       'NonCreditCAPSLast7Days': 'numeric',
                       'NonCreditCAPSLast90Days': 'numeric',
                       'Outstanding_Balance_All': 'numeric',
                       'Outstanding_Balance_Secured': 'numeric',
                       'Outstanding_Balance_Secured_Percentage': 'numeric',
                       'Outstanding_Balance_UnSecured': 'numeric',
                       'Outstanding_Balance_UnSecured_Percentage': 'numeric',
                       'TotalCAPSLast180Days': 'numeric',
                       'TotalCAPSLast30Days': 'numeric',
                       'TotalCAPSLast7Days': 'numeric',
                       'TotalCAPSLast90Days': 'numeric'
                       },
    'make_index': False,
    'time_index': None
}

CAIS_Account_DETAILS_config = {'entity_id':'CAIS_Account',
                'index':'CAIS_Account_id',
                'variable_types':{
              'AccountHoldertypeCode':'ordinal',
              'Open_Date':'date_of_birth',
              'Account_Type':'ordinal',
              'Portfolio_Type':'ordinal',
              'DateOfAddition':'datetime',
              'Payment_Rating':'ordinal',
              'Written_Off_Amt_Total':'numeric',
              'Date_Reported':'datetime',
              'Date_Closed':'datetime',
              'Current_Balance':'numeric',
              'Amount_Past_Due':'numeric',
              'Rate_of_Interest':'numeric',
              'Terms_Frequency':'ordinal',
              'Date_of_Last_Payment':'datetime',
              'Highest_Credit_or_Original_Loan_Amount':'numeric',
              'Settlement_Amount':'numeric',
              'Written_Off_Amt_Principal':'numeric',
              'Repayment_Tenure':'numeric',
              'Terms_Duration':'numeric',
              'Account_Status':'ordinal'},
              'make_index':False,
              'time_index':None
         }

CAPS_Application_Details_config = {'entity_id': 'CAPS_Application',
                                   'index': 'CAPS_Application_id',
                                   'variable_types': {'Date_of_Request': 'datetime',
                                                      'Enquiry_Reason': 'categorical',
                                                      'Amount_Financed': 'numeric',
                                                      'Duration_Of_Agreement': 'numeric',
                                                      'Finance_Purpose': 'categorical',
                                                      'Telephone_Type': 'categorical',
                                                      'Gender_Code': 'categorical',
                                                      'Date_Of_Birth_Applicant': 'date_of_birth',
                                                      'MobilePhoneNumber': 'phone_number'},
                                   'make_index': False,
                                   'time_index': None
                                   }

CAIS_Account_History_config = {
    'entity_id': 'CAIS_Account_History',
    'index': 'CAIS_Account_History_id',
    'variable_types': {
        'Days_Past_Due': 'numeric',
        'Month': 'ordinal',
        'Asset_Classification': 'ordinal',
        'Year': 'numeric'},
    'make_index': False,
    'time_index': None
}