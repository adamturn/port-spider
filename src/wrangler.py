"""
Python 3.7
Author: Adam Turner <turner.adch@gmail.com>
"""

# python package index
import numpy as np
# conda-forge
import camelot
# standard library
import re
from copy import deepcopy


class TableConfig(object):

    def __init__(self, cols=None, start=None, end=None):
        self.cols = cols
        self.start = start
        self.end = end
        self.df = None
    

class Wrangler(object):

    @staticmethod
    def __define_table_configs():
        std_cfg = TableConfig(cols=['dock_arrival', 'flag', 'last_port', 'loa', 'eta', 'etd', 'dock', 'service', 'agent'])
        table_names = ['in port', 'anchorage', 'vessels due', 'amfels', 'barges in port']
        tables = {name: deepcopy(std_cfg) for name in table_names}
        # >>> 
        # REPLACE STANDARD CONFIGS HERE
        barge_cfg = TableConfig(cols=['arrival', 'barge', 'tug', 'dock', 'service', 'agent'])
        tables['barges in port'] = barge_cfg
        # <<<
        return tables

    @staticmethod
    def parse_pdf(file_path):
        tables = Wrangler.__define_table_configs()
        date_regex = re.compile(r"(\d{1,2}\/){2}\d{4}")
        notes_regex = re.compile(r"notes:?", flags=re.IGNORECASE)

        print("Processing PDF...")
        parsed_tables = camelot.read_pdf(filepath=file_path, pages='1-end')
        for i, tbl in enumerate(parsed_tables):
            print(f"\nParsing page {i+1}.")
            df = tbl.df
            # this following line is mainly for debugging purposes to see if table start/end matches index
            # it will export these csv files to the project root directory
            # df.to_csv(f"parsed-table-{i}.csv")
            column_a = df.iloc[:, 0]

            cache = {'last': None, 'history': []}
            for i, cell in column_a.items():
                cell = cell.strip().lower()

                # basic logic for parsing one of these tables is as follows...
                # step 1: find a matching table name, save to cache['last']
                # step 2: find the next date cell, save start row as i
                # step 3: find the 'Notes:' cell, save end row as i-1 (blank row)
                # step 4: empty cache['last'], return to step 1

                if cache['last']:
                    if tables[cache['last']].start:
                        if notes_regex.search(cell):
                            print(f"  > last row for \'{cache['last']}\': {i}")
                            tables[cache['last']].end = i-1
                            cache['history'].append(cache['last'])
                            cache['last'] = None
                        else:
                            continue
                    else:
                        if date_regex.search(cell):
                            print(f"  > first row for \'{cache['last']}\': {i}")
                            tables[cache['last']].start = i
                        else:
                            continue
                else:
                    if cell in tables:
                        print(f"Found \'{cell}\' table!")
                        cache['last'] = cell
                    else:
                        continue

            # now cache['history'] is a list of str table names that we parsed from this tbl
            print("\nBuilding DataFrames...")
            for name in cache['history']:
                start_row = tables[name].start
                end_row = tables[name].end
                print(f"  > \'{name}\' rows: {start_row} to {end_row}")

                tables[name].df = df.iloc[start_row:end_row, :].copy()
                t_df = tables[name].df
                t_df.replace(to_replace=r"^\s*$", value=np.nan, regex=True, inplace=True)
                t_df.dropna(axis=0, how='all', inplace=True)
                t_df.dropna(axis=1, how='all', inplace=True)
                t_df.replace(to_replace=r"\n", value=" ", regex=True, inplace=True)

                num_parsed_cols = t_df.shape[1]
                expected_cols = tables[name].cols
                if num_parsed_cols == len(expected_cols):
                    t_df.columns = expected_cols
                else:
                    # TODO: if it doesn't match, raise a warning and skip it for now? (ask Roberto)
                    print(f"WARNING: Column length mismatch! # of parsed cols: {num_parsed_cols}, # of expected cols: {len(expected_cols)}")
            continue

        print("\nFinished parsing!")
        for table in tables:
            print(f"\n\'{table}\' DataFrame:\n{tables[table].df.head()}")

        return tables
