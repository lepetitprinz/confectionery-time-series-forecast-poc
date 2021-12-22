import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from baseline.deployment.PipelineReal import PipelineReal

# Sales Data configuration
division = 'SELL_IN'    # SELL_IN / SELL_OUT
in_out = 'out'    # SELL-IN : out / in
cycle = 'w'    # SELL-OUT : w(week) / m(month)

test_vrsn_cd = 'TEST_SELL_IN_BRAND'

# Execute Configuration
step_cfg = {
    'cls_load': True,
    'cls_cns': False,
    'cls_prep': False,
    'cls_train': False,
    'cls_pred': False,
    'clss_mdout': False,
    'cls_rpt': False
}

# Configuration
exec_cfg = {
    'cycle': False,
    'save_step_yn': True,            # Save each step result to object or csv
    'save_db_yn': False,             #
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
    'test_vrsn_cd': test_vrsn_cd,
    'date': {
        'history': {
            'from': '20201102',
            'to': '20211031'
        },
        'middle_out': {
            'from': '20210802',
            'to': '20211031'
        },
        'evaluation': {
            'from': '20211101',
            'to': '20220130'
        }
    }
}

# Load result configuration
exec_rslt_cfg = {
    'train': True,
    'predict': True,
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
    unit_cfg=unit_cfg
)

# Execute Baseline Forecast
pipeline.run()