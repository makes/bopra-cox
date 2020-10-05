import subprocess
import papermill as papermill

import os
import glob
from shutil import copyfile

ANALYSIS_STEP = "4"
ANALYSIS_STEP_NAME = ANALYSIS_STEP + "_plot_map_rso2"

# discarding cases 4, 11 and 12 as they did not contain IBP data
CASE_IDS = [1, 2, 3, 5, 6, 7, 8, 9, 10]
TEMPLATE_NOTEBOOK = ANALYSIS_STEP_NAME + '.ipynb'

OUTPUT_DIR = './reports/'
PUBLISH_DIR = 'Z:/public_html/bopra/reports/' + ANALYSIS_STEP_NAME

def run_notebook(case_ids, template_notebook):
    for case_id in case_ids:
        name = str(case_id).zfill(5)
        outfile = os.path.join(OUTPUT_DIR, f"{ANALYSIS_STEP}_{name}.ipynb")
        papermill.execute_notebook(
            template_notebook,
            outfile,
            parameters=dict(case_id=case_id),
        )
        generate_html_report(outfile)

def generate_html_report(notebook_file):
    _ = subprocess.run(
        ["jupyter", "nbconvert", notebook_file, "--to=html"]
    )

def publish_html(case_ids):
    for case_id in case_ids:
        name = str(case_id).zfill(5)
        src = os.path.join(OUTPUT_DIR, ANALYSIS_STEP + "_" + name + ".html")
        dst = os.path.join(PUBLISH_DIR, ANALYSIS_STEP + "_" + name + ".html")
        copyfile(src, dst)

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    run_notebook(CASE_IDS, TEMPLATE_NOTEBOOK)

    if not os.path.exists(PUBLISH_DIR):
        os.makedirs(PUBLISH_DIR)
    publish_html(CASE_IDS)

if __name__ == "__main__":
    main()

