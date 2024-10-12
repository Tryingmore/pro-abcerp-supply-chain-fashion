
@echo off

e:

cd E:/www/w_dev/w_a_abcerp/v1/v1.0_abcerp16

call venv_dev2/Scripts/activate
 
echo Stopping Erp 16...

::python abcerp-bin -c abcerp_dev2.conf --dev=all

pause
