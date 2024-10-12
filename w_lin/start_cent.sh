#!/usr/env/bin bash
cd /home/www/w_pro/pro_uperp/codes/v1.0_uperp16/
source venv_ts/bin/activate
python3 uperp-bin -c uperp_ts.conf --dev=all
