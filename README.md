# Cerebral oximetry data analysis pipeline

Analysis and reporting framework to study the relationship between cerebral tissue oximetry (rSO<sub>2</sub>) and mean arterial pressure (MAP).

1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Usage](#usage)
3. [Project Files](#project-files)
4. [Output CSV Format](#output-csv-format)

## Requirements

[Miniconda or anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html) installation.

## Setup

Clone the repository to your computer:

    git clone https://github.com/makes/bopra.git
    cd bopra

To install the required sofware packages, run the following command that creates a conda environment.

    conda env create --name bopra-cox --file environment.yml

or, to store the environment under project folder, you can use

    conda env create --prefix ./env --file environment.yml

Activate the installed environment using

    conda activate bopra-cox

or, if you installed the environment under project folder,

    conda activate ./env

## Usage

Copy the raw data files into the `data` folder. NIRS files must be named `nirs[case id].csv`. ZOLL files must be named `zoll[case id].json`.

The `amend` folder must contain the files `[case id]_a1.csv`, `[case id]_a2.csv` and `timeshift.csv`. `*_a1.csv` are comma delimited files containing column `Bad_MAP_manual` to exclude invalid MAP readings. `*_a2.csv` are semicolon separated files containing column `HuonoSignaali2` to exclude invalid NIRS readings.

    ├─data
    │     nirs00001.csv
    │     zoll00001.json
    │     nirs00002.csv
    │     zoll00002.json
    |     ...
    ├─amend
    │     timeshift.csv
    │     00001_a1.csv
    │     00001_a2.csv
    │     00002_a1.csv
    │     00002_a2.csv
    |     ...

In `config.ini`, specify which `CaseIds` to process in each step. This allows for exclusion of datasets.

To execute all steps for all the cases, use the script `runall.ps1`. To do partial runs, use the `process.py` script. Image assets are stored in the `reports/images` folder. The `report_visuals.py` script gathers the image assets to markdown files for easy viewing. The `reports` folder is a self contained website for easy publishing.

## Project files

    │ *.ipynb
    │ anonymize.py
    │ config.ini
    │ environment.yml
    │ process.py
    │ README.md
    │ report_visuals.py
    │ runall.ps1
    ├───adhoc
    ├───amend
    ├───data
    ├───doc
    ├───output
    ├───reports
    │   ├───images
    │   ├───markdown
    │   └───notebooks
    └───utils

`environment.yml` specifies the `conda` environment, and what software packages to install. See section [setup](#setup) for instructions.

`runall.ps1`: A script to execute the entire pipeline from start to finish. Can be run in Anaconda Powershell prompt.

`*.ipynb`: The Jupyter notebooks for each analysis step. Used as papermill templates.

`process.py`: A script to process an analysis step. Usage: `python process.py <step>` for all cases defined in `config.ini`. To select a single case for processing, use the `--case <id>` argument. Uses papermill to do the work.

`report_visuals.py` outputs markdown to display the generated image assets.

`anonymize.py`: A script to obfuscate timestamps in data to prevent identification.

`data`: A folder containing input data - NIRS CSV and ZOLL JSON.

`amend`: A folder containing manually crafted additions to the data, i.e. markings for artefact removal and synchronization.

`output`: Output CSV, intermediate and final.

`reports`: Output directory for image assets and reports. This directory can be hosted on a PHP enabled web server for easy sharing. To view locally, PHP's built in web server can be used: `php -S localhost:8000`.

`utils`: Python modules containing helper functions for data loading and processing.

`adhoc`: Test scripts and other throwaway code.

`doc`: Additional documentation (Excel workbooks).

## Output CSV format

Missing values are denoted by '-'. Time resolution is 1 second.

- `Time`: Timestamp in format H:M:S, starting at 00:00:00
- `MAP`: Mean arterial pressure computed from pulse waveform using a 10 second moving average
- `Bad_MAP_auto`: `1` indicated blood pressure values marked invalid by the monitoring device, `0` otherwise
- `Bad_MAP_manual`: `1` indicated blood pressure values manually marked invalid, `0` otherwise.
- `rSO2`: Cerebral tissue oxygen saturation percentage measured using NIRS. Resolution 1 %.
- `Mark`: Value `1` indicates start of anaesthesia, `0` otherwise
- `Bad_rSO2_auto`: `1` indicated rSO<sub>2</sub> values marked invalid by the monitoring device, `0` otherwise
- `Bad_rSO2_manual`: `1` indicated rSO<sub>2</sub> values manually marked invalid, `0` otherwise
- `COx`: "Cerebral oximetry index" calculated using a 300 second rolling correlation between MAP and rSO<sub>2</sub>, with bad input values dropped out and imputed by linear interpolation.
- `MAP_delay`: The first value of this column indicates the MAP delay that was used to synchronize the input signals.