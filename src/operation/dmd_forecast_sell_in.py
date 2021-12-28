import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from baseline.deployment.PipelineCycle import PipelineCycle

# Sales Data configuration
division = 'SELL_IN'    # SELL_IN / SELL_OUT
in_out = 'out'    # SELL-IN : out / in
cycle = 'w'    # SELL-OUT : w(week) / m(month)

path_root = os.path.join('/', 'opt', 'DF', 'fcst')

test_vrsn_cd = 'BASELINE_CYCLE'

# Data Configuration
data_cfg = {
    'division': division,
    'in_out': in_out,
    'cycle': cycle,
    'test_vrsn_cd': test_vrsn_cd
}

# Configuration
exec_cfg = {
    'cycle': True,
    'save_step_yn': True,            # Save each step result to object or csv
    'save_db_yn': True,              # Save each step result to Database
    'decompose_yn': False,           # Decomposition
    'rm_not_exist_lvl_yn': False,    # Remove not exist data level
    'scaling_yn': False,             # Data scaling
    'impute_yn': True,               # Data Imputation
    'rm_outlier_yn': True,           # Outlier Correction
    'feature_selection_yn': False,   # Feature Selection
    'grid_search_yn': False          # Grid Search
}

# Execute Configuration
step_cfg = {
    'cls_load': True,
    'cls_cns': True,
    'cls_prep': True,
    'cls_train': True,
    'cls_pred': True,
    'clss_mdout': True,
    'cls_rpt': True
}

# Load result configuration
exec_rslt_cfg = {
    'train': False,
    'predict': False,
    'middle_out': False
}

# Unit Test Option
unit_cfg = {'unit_test_yn': False}

pipeline = PipelineCycle(
    data_cfg=data_cfg,
    exec_cfg=exec_cfg,
    step_cfg=step_cfg,
    exec_rslt_cfg=exec_rslt_cfg,
    unit_cfg=unit_cfg,
    path_root=path_root
)

# Execute Baseline Forecast
# pipeline.run()