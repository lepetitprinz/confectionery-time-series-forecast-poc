import os
import sys
import time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from baseline.deployment.PipelineReal import PipelineReal


# Root path
path_root = os.path.join('/', 'opt', 'DF', 'fcst')

# Sales Data configuration
division = 'SELL_IN'    # SELL_IN / SELL_OUT
in_out = 'out'    # SELL-IN : out / in
cycle = 'w'    # SELL-OUT : w(week) / m(month)
item_lvl = 3 # 3: brand

test_vrsn_cd = 'TEST_1228_SELL_IN_2YEAR_BRAND'

# Execute Configuration
step_cfg = {
    'cls_load': False,
    'cls_cns': True,
    'cls_prep': True,
    'cls_train': True,
    'cls_pred': True,
    'clss_mdout': True,
    'cls_rpt': False
}

# Configuration
exec_cfg = {
    'cycle': False,
    'save_step_yn': True,            # Save each step result to object or csv
    'save_db_yn': True,             #
    'rm_not_exist_lvl_yn': False,    # Remove not exist data level
    'decompose_yn': False,           # Decomposition
    'scaling_yn': False,             # Data scaling
    'impute_yn': True,               # Data Imputation
    'rm_outlier_yn': True,           # Outlier Correction
    'feature_selection_yn': False,   # Feature Selection
    'grid_search_yn': False,          # Grid Search
    'filter_threshold_week_yn': False,
    'rm_fwd_zero_sales_yn': True
}

# Data Configuration
data_cfg = {
    'division': division,
    'in_out': in_out,
    'cycle': cycle,
    'item_lvl': item_lvl,
    'test_vrsn_cd': test_vrsn_cd,
    'date': {
        'history': {
            'from': '20191223', # 20191223 for two years / 20201228 for one year
            'to': '20211226'
        },
        'middle_out': {
            'from': '20210927',
            'to': '20211226'
        },
        'evaluation': {
            'from': '20211227',
            'to': '20220327'
        }
    }
}

# Load result configuration
exec_rslt_cfg = {
    'train': False,
    'predict': False,
    'middle_out': False
}

# Unit Test Option
unit_cfg = {
    'unit_test_yn': False,
    'cust_grp_cd': '1202',
    'item_cd': '5100000'
}


pipeline = PipelineReal(
    data_cfg=data_cfg,
    exec_cfg=exec_cfg,
    step_cfg=step_cfg,
    exec_rslt_cfg=exec_rslt_cfg,
    unit_cfg=unit_cfg,
    path_root=path_root
)

start_time = time.time()
print(test_vrsn_cd)
# Execute Baseline Forecast
pipeline.run()

end_time = time.time()

print('running time: ', end_time - start_time)