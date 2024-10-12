#!/usr/env/bin bash
cd /home/www/w_pro/pro_uperp/codes/v1.0_uperp16/
source venv_ts/bin/activate
#source venv_sho/bin/activate
#source venv_prd/bin/activate
python3 uperp-bin -c uperp_ts.conf --dev=all
