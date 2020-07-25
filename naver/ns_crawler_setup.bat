@echo off
pip uninstall -y requests
pip uninstall -y bs4
pip uninstall -y pandas

pip install requests
pip install bs4
pip install pandas

echo ***** PIP Install is complete *****
