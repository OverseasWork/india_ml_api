import pandas as pd
import datetime
import string
import numpy as np
from .utils.util import loan_dt, stamp_format, prob2Score, \
    load_model, load_txt_feat
import sys

sys.path.append('..')


class AppListML:
    """appList模型主程序"""

    def __init__(self):
        self.file = 'app/app/applist_ml/data/'
        self.lgb = load_model(self.file + 'gbm_finall.pkl')
        self.appname = load_txt_feat(self.file + 'competitive_appname.txt')
        self.col = load_txt_feat(self.file + 'in_ml_col.txt')
        self.comp = pd.read_excel(self.file + 'competitive_package.xlsx')

    def get_params(self, data, days, comp):
        d7_data = data[data['firstInstallTime'] > data['apply_date'] - datetime.timedelta(days)]
        d1 = d7_data.groupby('reqId').agg({'packageName': pd.Series.nunique, 'appName': pd.Series.nunique})  #
        d7_data2 = data[
            (data['firstInstallTime'] > data['apply_date'] - datetime.timedelta(days)) & (data.packageName.isin(comp))]
        d2 = d7_data2.groupby('reqId').agg({'packageName': pd.Series.nunique, 'appName': pd.Series.nunique})  #
        d1.columns = ['package_cnt_%sd' % days, 'app_cnt_%sd' % days]  #
        d2.columns = ['comp_package_cnt_%sd' % days, 'comp_app_cnt_%sd' % days]  #
        d3 = pd.merge(d1, d2, left_index=True, right_index=True, how='left')
        d3['comp_package_rate_%sd' % days] = d3['comp_package_cnt_%sd' % days] / d3['package_cnt_%sd' % days]
        d3['comp_app_rate_%sd' % days] = d3['comp_app_cnt_%sd' % days] / d3['app_cnt_%sd' % days]
        return d3

    def re_db(self, data):

        s = pd.DataFrame(index=data.reqId.unique())
        for i in [3, 7, 15, 30, 60, 90, 180]:
            res = self.get_params(data, i, self.comp.package_name.unique())
            s = pd.merge(s, res, left_index=True, right_index=True, how='left')
        all_data = pd.merge(s, data[['reqId']], left_index=True, right_on='reqId', how='left')
        all_cnt = data.groupby('reqId').agg(
            {'packageName': pd.Series.nunique, 'appName': pd.Series.nunique}).reset_index()
        all_cnt.columns = ['reqId', 'package_all_cnt', 'app_all_cnt']
        all_comp = data[data.packageName.isin(self.comp.package_name.unique())].groupby('reqId').agg(
            {'packageName': pd.Series.nunique, 'appName': pd.Series.nunique}).reset_index()
        all_comp.columns = ['reqId', 'package_all_comp_cnt', 'app_all_comp_cnt']
        all_data2 = pd.merge(all_data, all_cnt, on='reqId', how='left')
        all_data3 = pd.merge(all_data2, all_comp, on='reqId', how='left')
        all_data3['package_install_rate_3d'] = all_data3['package_cnt_3d'] / all_data3['package_all_cnt']
        all_data3['package_install_rate_7d'] = all_data3['package_cnt_7d'] / all_data3['package_all_cnt']
        all_data3['package_install_rate_15d'] = all_data3['package_cnt_15d'] / all_data3['package_all_cnt']
        all_data3['package_install_rate_30d'] = all_data3['package_cnt_30d'] / all_data3['package_all_cnt']
        all_data3['package_install_rate_60d'] = all_data3['package_cnt_60d'] / all_data3['package_all_cnt']
        all_data3['package_install_rate_90d'] = all_data3['package_cnt_90d'] / all_data3['package_all_cnt']
        all_data3['package_install_rate_180d'] = all_data3['package_cnt_180d'] / all_data3['package_all_cnt']

        all_data3['app_install_rate_3d'] = all_data3['app_cnt_3d'] / all_data3['app_all_cnt']
        all_data3['app_install_rate_7d'] = all_data3['app_cnt_7d'] / all_data3['app_all_cnt']
        all_data3['app_install_rate_15d'] = all_data3['app_cnt_15d'] / all_data3['app_all_cnt']
        all_data3['app_install_rate_30d'] = all_data3['app_cnt_30d'] / all_data3['app_all_cnt']
        all_data3['app_install_rate_60d'] = all_data3['app_cnt_60d'] / all_data3['app_all_cnt']
        all_data3['app_install_rate_90d'] = all_data3['app_cnt_90d'] / all_data3['app_all_cnt']
        all_data3['app_install_rate_180d'] = all_data3['app_cnt_180d'] / all_data3['app_all_cnt']

        all_data3['comp_normal_pack_rate_3d'] = all_data3['comp_package_cnt_3d'] / (
                all_data3['package_cnt_3d'] - all_data3['comp_package_cnt_3d'])
        all_data3['comp_normal_pack_rate_7d'] = all_data3['comp_package_cnt_7d'] / (
                all_data3['package_cnt_7d'] - all_data3['comp_package_cnt_7d'])
        all_data3['comp_normal_pack_rate_15d'] = all_data3['comp_package_cnt_15d'] / (
                all_data3['package_cnt_15d'] - all_data3['comp_package_cnt_15d'])
        all_data3['comp_normal_pack_rate_30d'] = all_data3['comp_package_cnt_30d'] / (
                all_data3['package_cnt_30d'] - all_data3['comp_package_cnt_30d'])
        all_data3['comp_normal_pack_rate_60d'] = all_data3['comp_package_cnt_60d'] / (
                all_data3['package_cnt_60d'] - all_data3['comp_package_cnt_60d'])
        all_data3['comp_normal_pack_rate_90d'] = all_data3['comp_package_cnt_90d'] / (
                all_data3['package_cnt_90d'] - all_data3['comp_package_cnt_90d'])
        all_data3['comp_normal_pack_rate_180d'] = all_data3['comp_package_cnt_180d'] / (
                all_data3['package_cnt_180d'] - all_data3['comp_package_cnt_180d'])

        all_data3['comp_normal_app_rate_3d'] = all_data3['comp_app_cnt_3d'] / (
                all_data3['app_cnt_3d'] - all_data3['comp_app_cnt_3d'])
        all_data3['comp_normal_app_rate_7d'] = all_data3['comp_app_cnt_7d'] / (
                all_data3['app_cnt_7d'] - all_data3['comp_app_cnt_7d'])
        all_data3['comp_normal_app_rate_15d'] = all_data3['comp_app_cnt_15d'] / (
                all_data3['app_cnt_15d'] - all_data3['comp_app_cnt_15d'])
        all_data3['comp_normal_app_rate_30d'] = all_data3['comp_app_cnt_30d'] / (
                all_data3['app_cnt_30d'] - all_data3['comp_app_cnt_30d'])
        all_data3['comp_normal_app_rate_60d'] = all_data3['comp_app_cnt_60d'] / (
                all_data3['app_cnt_60d'] - all_data3['comp_app_cnt_60d'])
        all_data3['comp_normal_app_rate_90d'] = all_data3['comp_app_cnt_90d'] / (
                all_data3['app_cnt_90d'] - all_data3['comp_app_cnt_90d'])
        all_data3['comp_normal_app_rate_180d'] = all_data3['comp_app_cnt_180d'] / (
                all_data3['app_cnt_180d'] - all_data3['comp_app_cnt_180d'])

        all_data3['comp_package_install_rate_3d'] = all_data3['comp_package_cnt_3d'] / all_data3['package_all_comp_cnt']
        all_data3['comp_package_install_rate_7d'] = all_data3['comp_package_cnt_7d'] / all_data3['package_all_comp_cnt']
        all_data3['comp_package_install_rate_15d'] = all_data3['comp_package_cnt_15d'] / all_data3[
            'package_all_comp_cnt']
        all_data3['comp_package_install_rate_30d'] = all_data3['comp_package_cnt_30d'] / all_data3[
            'package_all_comp_cnt']
        all_data3['comp_package_install_rate_60d'] = all_data3['comp_package_cnt_60d'] / all_data3[
            'package_all_comp_cnt']
        all_data3['comp_package_install_rate_90d'] = all_data3['comp_package_cnt_90d'] / all_data3[
            'package_all_comp_cnt']
        all_data3['comp_package_install_rate_180d'] = all_data3['comp_package_cnt_180d'] / all_data3[
            'package_all_comp_cnt']

        all_data3['comp_app_install_rate_3d'] = all_data3['comp_app_cnt_3d'] / all_data3['app_all_comp_cnt']
        all_data3['comp_app_install_rate_7d'] = all_data3['comp_app_cnt_7d'] / all_data3['app_all_comp_cnt']
        all_data3['comp_app_install_rate_15d'] = all_data3['comp_app_cnt_15d'] / all_data3['app_all_comp_cnt']
        all_data3['comp_app_install_rate_30d'] = all_data3['comp_app_cnt_30d'] / all_data3['app_all_comp_cnt']
        all_data3['comp_app_install_rate_60d'] = all_data3['comp_app_cnt_60d'] / all_data3['app_all_comp_cnt']
        all_data3['comp_app_install_rate_90d'] = all_data3['comp_app_cnt_90d'] / all_data3['app_all_comp_cnt']
        all_data3['comp_app_install_rate_180d'] = all_data3['comp_app_cnt_180d'] / all_data3['app_all_comp_cnt']
        all_data3.drop_duplicates(inplace=True)
        all_data3.replace(np.inf, 0, inplace=True)
        all_data3.fillna(0, inplace=True)
        return all_data3

    def applist_ml_predict(self, data: dict):
        """
        """
        appList = data['data']
        i1 = [[data['reqId'], i['appName'], i['packageName'], i['firstInstallTime'], i['lastUpdateTime']]
              for i in appList]
        res_data = pd.DataFrame(i1, columns=['reqId', 'appName', 'packageName', 'firstInstallTime',
                                             'lastUpdateTime'])
        res_data['firstInstallTime'] = res_data['firstInstallTime'].apply(stamp_format)
        res_data['lastUpdateTime'] = res_data['lastUpdateTime'].apply(stamp_format)
        res_data['apply_date'] = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
        res_data.firstInstallTime = pd.to_datetime(res_data.firstInstallTime)
        res_data.lastUpdateTime = pd.to_datetime(res_data.lastUpdateTime)
        res_data.apply_date = pd.to_datetime(res_data.apply_date)
        res_data['appName'] = res_data['appName'].apply(lambda x: str(x).lower())
        res_data['appName'] = res_data['appName'].apply(
            lambda x: ''.join(x for x in x.split() if x not in string.punctuation))
        res_data['appName'] = res_data['appName'].str.replace('[^\w\s]', '')
        res_data['appName'] = res_data['appName'].apply(
            lambda x: ''.join(x for x in x.split() if not x.isdigit()))
        res_data2 = self.re_db(res_data)
        comp = [i.strip() for i in self.appname]
        test_matrix = pd.DataFrame(columns=comp, index=[data['reqId']])
        for i in res_data[['reqId', 'appName']].values.tolist():
            if i[1] in comp:
                test_matrix.loc[i[0], i[1]] = 1
        res_data3 = pd.merge(res_data2, test_matrix, left_on='reqId', right_index=True, how='left')
        colum = [i.rstrip() for i in self.col]
        res_data4 = res_data3[colum]
        res_data4.fillna(0, inplace=True)
        preds = self.lgb.predict_proba(res_data4)[:, 1][0]
        score = prob2Score(preds)
        return {'reqId': data['reqId'], 'prob': round(preds, 2), 'score': int(score), 'msg': 'success',
                'data': {k: str(v) for k, v in res_data2.to_dict(orient='records')[0].items()}}
