import papermill as papermill
import subprocess

import argparse
import configparser
import json

import os

def run_notebook(step, name, case_ids, outdir):
    template_nb = str(step) + f'_{name}.ipynb'
    for case_id in case_ids:
        outname = str(case_id).zfill(5)
        outfile = os.path.join(outdir, f"{step}_{outname}.ipynb")
        papermill.execute_notebook(
            template_nb,
            outfile,
            parameters=dict(case_id=case_id),
        )
        generate_html_report(outfile)

def generate_html_report(notebook_file):
    _ = subprocess.run(
        ["jupyter", "nbconvert", notebook_file, "--to=html"]
    )

def main():
    # handle command line arguments
    arg_parser = argparse.ArgumentParser(description='''
        Process analysis step.
        Executes relevant Jupyter notebook for each case defined in config.ini
        and stores output .ipynb and .html.
        Use the --case=<id> argument to choose a single case for processing.
        ''')
    arg_parser.add_argument('step',
                            metavar='STEP',
                            type=int,
                            nargs=1,
                            help='analysis step id')
    arg_parser.add_argument('--case', dest='case', type=int, help='case id')
    args = arg_parser.parse_args()

    # read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')

    # get args and config
    step = args.step[0]
    stepcfg = config['Step' + str(step)]
    name = stepcfg['Name']
    cases = json.loads(stepcfg['CaseIds'])
    if args.case is not None:
        cases = [args.case]
    reportdir = config['Global']['ReportDir']
    nbdir = config['ReportSubdirs']['Notebooks']
    outdir = os.path.join(reportdir, nbdir)
    print(f'Processing step {step} for cases {cases}')

    # process
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    run_notebook(step, name, cases, outdir)

if __name__ == "__main__":
    main()
