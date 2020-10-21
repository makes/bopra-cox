import argparse
import configparser
import json

import glob
import os

def generate_markdown(imgpath, step, case_ids, imgdir):
    output = ''
    for case_id in case_ids:
        md = f'## Case {str(case_id).zfill(5)}:\n\n'
        flt = f'{str(step)}_{str(case_id).zfill(5)}_*.png'
        flt = os.path.join(imgpath, flt)
        case_images = sorted(glob.glob(flt))
        for path in case_images:
            filename = os.path.basename(path)
            href = imgdir + filename
            md += f'![]({href})\n'
        output += md + '\n'
    return output

def main():
    # handle command line arguments
    arg_parser = argparse.ArgumentParser(description='''
        Generate markdown containing all visualizations for the step specified as argument.
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
    stepname = config['Step' + str(step)]['Name']
    cases = json.loads(config['Step' + str(step)]['CaseIds'])
    if args.case is not None:
        cases = [args.case]
    reportdir = config['Global']['ReportDir']
    imgdir = config['ReportSubdirs']['Images']
    mddir = config['ReportSubdirs']['Markdown']
    imgpath = os.path.join(reportdir, imgdir)
    mdpath = os.path.join(reportdir, mddir)
    print(f'Generating visualization report for {step}, cases {cases}')

    # process
    markdown = f'# {str(step)}: {stepname}\n\n'
    markdown += '[Back](analysis.php)\n\n'
    if not os.path.exists(mdpath):
        os.makedirs(mdpath)
    markdown += generate_markdown(imgpath, step, cases, imgdir)

    outfile = os.path.join(mdpath, f'{str(step)}_images.md')
    f = open(outfile, 'w')
    f.write(markdown)
    f.close()

if __name__ == "__main__":
    main()
