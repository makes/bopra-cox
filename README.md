# Data analysis pipeline - Cerebral oximetry

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