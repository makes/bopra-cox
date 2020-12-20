#!/usr/bin/env pwsh

#python process.py 1
python process.py 2
python process.py 3
python process.py 4
python process.py 5
python process.py 6
python process.py 7
python process.py 8
python process.py 9
#python report_visuals.py 1
python report_visuals.py 2
python report_visuals.py 3
python report_visuals.py 4
python report_visuals.py 5
python report_visuals.py 6
python report_visuals.py 7
python report_visuals.py 8
jupyter nbconvert ./reports/notebooks/9_00000.ipynb --to=html --output="../stats.html"
