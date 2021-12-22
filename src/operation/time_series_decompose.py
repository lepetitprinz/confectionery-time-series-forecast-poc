import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from baseline.deployment.PipelineDecompCycle import PipelineDecompCycle

# Data Configuration
data_cfg = {
    'division': 'SELL_IN',
    'in_out': 'out',
    'cycle': 'w',
}

# Execute Configuration
exec_cfg = {
    'cycle': True,
    'save_step_yn': True,            # Save each step result to object or csv
    'save_db_yn': True,              # Save DB
    'decompose_yn': True,            # Decomposition
    'impute_yn': True,               # Data Imputation
    'rm_outlier_yn': True,           # Outlier Correction
    'feature_selection_yn': False,
    'rm_not_exist_lvl_yn': False
}

# Brand Level
pipeline_brand = PipelineDecompCycle(
    data_cfg=data_cfg,
    exec_cfg=exec_cfg,
    item_lvl=3
)
pipeline_brand.run()

# Item Level
pipeline_item = PipelineDecompCycle(
    data_cfg=data_cfg,
    exec_cfg=exec_cfg,
    item_lvl=4
)
pipeline_item.run()