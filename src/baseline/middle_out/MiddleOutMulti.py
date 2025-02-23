import common.util as util
import common.config as config

import numpy as np
import pandas as pd
from copy import deepcopy


class MiddleOutMulti(object):
    def __init__(self, common: dict, division: str, data_vrsn: str, hrchy: dict,
                 mst_info: dict, item_mst: pd.DataFrame, ratio_lvl):
        # Data Information Configuration
        self.common = common
        self.division_cd = division
        self.data_vrsn_cd = data_vrsn
        # self.mst_info = mst_info
        self.model_list = [col.upper() for col in list(mst_info['model_mst'].keys())]

        # Data Level Configuration
        self.hrchy = hrchy
        self.hrchy_cust_cd_list = ['cust_grp_cd']
        self.hrchy_item_cd_list = common['db_hrchy_item_cd'].split(',')
        self.hrchy_item_nm_list = common['db_hrchy_item_nm'].split(',')
        self.hrchy_cd_to_db_cd = config.HRCHY_CD_TO_DB_CD_MAP
        self.drop_col = ['project_cd', 'division_cd', 'data_vrsn_cd', 'fkey', 'create_user_cd', 'accuracy'] + \
                         common['db_hrchy_item_nm'].split(',')

        # Middle-out Configuration
        self.err_val = 0
        self.max_val = 10 ** 5 - 1
        self.target_col = 'sales'
        self.item_mst = item_mst
        self.ratio_lvl = ratio_lvl
        self.split_lvl = self.hrchy['lvl']['item']

        # After processing Configuration
        self.rm_special_char_list = ['item_attr03_nm', 'item_attr04_nm', 'item_nm']

    def run_on_all_result(self, sales: pd.DataFrame, pred: pd.DataFrame):
        pred_dict = self.split_pred_by_model(data=pred)

        result = pd.DataFrame()
        for pred in pred_dict.values():
            md_out = self.exec_middle_out(sales=sales, pred=pred)
            result = pd.concat([result, md_out], axis=0)

        return result

    def filter_best_result(self, result: pd.DataFrame, score: pd.DataFrame):
        # convert columns to lower case
        result = util.conv_col_lower(data=result)
        score = util.conv_col_lower(data=score)

        # Drop unnecessary columns
        score = score.drop(columns=['rmse', 'accuracy', 'create_user_cd'], errors='ignore')

        merge_col = ['data_vrsn_cd', 'division_cd', 'stat_cd'] + \
                    [config.HRCHY_CD_TO_DB_CD_MAP.get(col, col) for col in self.hrchy['apply']]
        best_result = pd.merge(
            result,
            score,
            how='inner',
            on=merge_col,
            suffixes=('', '_DROP')
        ).filter(regex='^(?!.*_DROP)')

        return best_result

    def split_pred_by_model(self, data: pd.DataFrame) -> dict:
        data_split = {}
        for model in self.model_list:
            data_split[model] = data[data['stat_cd'] == model]

        return data_split

    def exec_middle_out(self, sales: pd.DataFrame, pred: pd.DataFrame) -> pd.DataFrame:
        data_split = self.prep_split(data=pred)
        data_ratio = self.prep_ratio(data=sales)
        middle_out = self.middle_out(data_split=data_split, data_ratio=data_ratio)
        middle_out_db = self.after_processing(data=middle_out)

        return middle_out_db

    def prep_ratio(self, data: pd.DataFrame) -> pd.DataFrame:
        item_temp = deepcopy(self.item_mst)
        item_col = [col for col in item_temp.columns if 'nm' not in col]
        item_temp = item_temp[item_col]

        merged = pd.merge(data, item_temp, how='left', on=['sku_cd'])
        ratio = self.agg_by_data_level(data_ratio=merged, item_col=item_col)
        ratio = ratio.rename(columns=config.HRCHY_CD_TO_DB_CD_MAP)

        return ratio

    def prep_split(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data.drop(columns=self.drop_col, errors='ignore')
        data = data.rename(columns={'result_sales': 'sales'})

        return data

    def middle_out(self, data_split, data_ratio):
        # Acyclic iteration
        count = self.ratio_lvl - self.hrchy['lvl']['item']
        ratio = self.ratio_iter(df_ratio=data_ratio)
        result = self.split_iter(dict_ratio=ratio, split=data_split)

        return result

    def after_processing(self, data: pd.DataFrame) -> pd.DataFrame:
        item_mst = self.item_mst
        item_mst.columns = [self.hrchy_cd_to_db_cd.get(col, col) for col in item_mst.columns]
        item_mst = item_mst.rename(columns={'sku_cd': 'item_cd', 'sku_nm': 'item_nm'})
        data = data.rename(columns={self.target_col: 'result_sales', 'sku_cd': 'item_cd'})

        # Merge item master
        merged = pd.merge(
            data,
            item_mst,
            how='left',
            on=self.hrchy_item_cd_list
        )
        # Add db information
        result = self.add_db_information(data=merged)

        # Remove Special Character
        for col in self.rm_special_char_list:
            if col in list(result.columns):
                result = util.remove_special_character(data=result, feature=col)

        # convert 'inf' or '-inf' to zero
        result['result_sales'] = np.nan_to_num(result['result_sales'].values, posinf=0, neginf=0)

        return result

    @staticmethod
    def agg_by_data_level(data_ratio: pd.DataFrame, item_col: list) -> pd.DataFrame:
        agg_col = ['cust_grp_cd'] + item_col
        data_agg = data_ratio.groupby(by=agg_col).mean()
        data_agg = data_agg.reset_index()

        return data_agg

    def add_db_information(self, data: pd.DataFrame) -> pd.DataFrame:
        data['project_cd'] = self.common['project_cd']
        data['data_vrsn_cd'] = self.data_vrsn_cd
        data['division_cd'] = self.division_cd
        data['fkey'] = 'C1-P5' + '-MIDDLE-OUT-' + data['cust_grp_cd'] + '-' + data['item_cd']
        # data['fkey'] = self.hrchy['key'] + 'MIDDLE-OUT-' + data['cust_grp_cd'] + '-' + data['item_cd']

        return data

    def add_del_information(self) -> dict:
        info = {
            'project_cd': self.common['project_cd'],
            'data_vrsn_cd': self.data_vrsn_cd,
            'division_cd': self.division_cd,
            'fkey': 'C1-P5-MIDDLE-OUT'
        }

        return info

    # Step 1. Group by lower level quantity
    def group_by_agg(self, df: pd.DataFrame, group_lvl: int):
        col_group = self.hrchy_cust_cd_list + self.hrchy_item_cd_list[:group_lvl]
        df_agg = df.groupby(by=col_group).sum()
        df_agg = df_agg.reset_index()

        return df_agg

    # Step2. Calculate ratio
    def calc_ratio(self, df_upper, df_lower):
        result = self.merge_df(left=df_upper, right=df_lower)
        result['ratio'] = result[self.target_col + '_' + 'lower'] / result[self.target_col + '_' + 'upper']

        # Convert inf or -inf to zeros
        result['ratio'] = np.nan_to_num(result['ratio'].values, posinf=0, neginf=0)

        result = self.drop_qty(df=result)

        return result

    def ratio_iter(self, df_ratio: pd.DataFrame) -> dict:
        agg_dict = self.agg_data(df=df_ratio)

        ratio_dict = {}
        for i in range(self.split_lvl, self.ratio_lvl):
            upper = agg_dict[i]
            lower = agg_dict[i+1]
            upper = self.rename_col(df=upper, lvl='upper')
            lower = self.rename_col(df=lower, lvl='lower')
            ratio = self.calc_ratio(df_upper=upper, df_lower=lower)
            ratio_dict[i] = ratio

        return ratio_dict

    def agg_data(self, df: pd.DataFrame) -> dict:
        agg_dict = {self.ratio_lvl: df}
        for i in range(self.ratio_lvl, self.split_lvl, -1):
            ratio_grp = self.group_by_agg(df=df, group_lvl=i-1)
            agg_dict[i-1] = ratio_grp

        return agg_dict

    def split_iter(self, dict_ratio: dict, split: pd.DataFrame) -> pd.DataFrame:
        count = self.ratio_lvl - self.split_lvl
        lvl = self.split_lvl
        while count != 0:
            split = self.split(dict_ratio=dict_ratio, split=split, lvl=lvl)
            lvl += 1
            count -= 1

        return split

    def split(self, dict_ratio: dict, split: pd.DataFrame, lvl: int) -> pd.DataFrame:
        ratio = dict_ratio[lvl]
        split_qty = self.split_qty(upper=split, lower=ratio, lvl=lvl)

        return split_qty

    def merge_df(self, left, right):
        on = list(left.columns)
        on.remove(self.target_col + '_' + 'upper')
        merged = pd.merge(left, right, on=on)

        return merged

    def rename_col(self, df: pd.DataFrame, lvl: str):
        df = df.rename(columns={self.target_col: self.target_col + '_' + lvl})
        return df

    def drop_qty(self, df):
        return df.drop(columns=[self.target_col + '_' + 'lower', self.target_col + '_' + 'upper'])

    def split_qty(self, upper: pd.DataFrame, lower: pd.DataFrame, lvl: int):
        on = self.hrchy_cust_cd_list + self.hrchy_item_cd_list[:lvl]
        split = pd.merge(upper, lower, on=on)
        split[self.target_col] = round(split[self.target_col] * split['ratio'], 2)

        # clip & round results
        split[self.target_col] = np.clip(split[self.target_col].values, 0, self.max_val)
        split[self.target_col] = np.round(split[self.target_col].values, 2)

        split = split.drop(columns='ratio')

        return split
