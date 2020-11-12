# Brownsville Port Spider
This spider crawls to the Brownsville port website and downloads their daily vessel schedule. It depends on Camelot which uses OpenCV to parse table patterns from PDF files.

## Conda Quickstart
To isolate this project, I recommend recreating my conda virtual environment:

$ cd spider-bvilport

$ conda env create -f environment.yml

This will create a conda environment called 'spider-bvilport'. To run the spider, activate this environment and run the main program in the /src directory from the project root.

$ conda activate spider-bvilport

(spider-bvilport)$ python src/main.py

## Airflow
To run this spider from Airflow, we can use the SSH Operator. First we need to get the path to the python interpreter in this conda environment:

$ conda activate spider-bvilport

(spider-bvilport)$ which python

The final command passed to the Operator will probably look something like this:

$ /home/adam/miniconda3/envs/spider-bvilport/bin/python /home/adam/svncos/spider-bvilport/src/main.py

## Third-Party Packages
- requests: HTTP library
- camelot-py: parses table structures from PDF files using OpenCV.
- numpy: useful np.nan object

If you try to run the code and get errors relating to something called 'Ghostscript', this is one of Camelot's dependencies. To check if you have Ghostscript installed:

$ ghostscript -v

Check out this link for more help installing Camelot: https://camelot-py.readthedocs.io/en/master/user/install.html#install

## General Documentation
### spider-bvilport/ (project root)
1. README.md: this document
2. environment.yml: conda environment config

### src/
1. main.py: main entrypoint for this project
2. path_helper.py: verifies the absolute path to this project's /src directory
3. spider.py: spider program
4. wrangler.py: deals with pdf parsing logic
5. xlsx_parser.py: work in progress
