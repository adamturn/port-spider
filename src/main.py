"""
Python 3.7
Author: Adam Turner <turner.adch@gmail.com>
"""

# standard library
import sys
import time
import random
import datetime
# local modules
from spider import Spider
from wrangler import Wrangler
from path_helper import get_src_dir_path


def get_history():
    """Download historical vessel schedules."""

    src_dir = get_src_dir_path(__file__)
    data_dir = src_dir.parent / "data"

    start_date = datetime.date(year=2020, month=1, day=1)
    end_date = datetime.date(year=2020, month=1, day=10)
    time_delta = datetime.timedelta(days=1)

    file_paths = []
    jocasta = Spider()
    while start_date <= end_date:
        time.sleep(random.randrange(0, 5, 1))
        file_path = jocasta.crawl(data_dir, date=start_date)
        file_paths.append(file_path)
        start_date += time_delta
        
    for file_path in file_paths:
        if file_path.endswith('.xlsx'):
            print("unhandled xlsx file!")

        elif file_path.endswith('.pdf'):
            tables = Wrangler.parse_pdf(file_path)

        else:
            raise ValueError(f"Unexpected file type: {file_path}")

    return None


def main():
    """Main spider program processes the latest vessel schedule."""

    src_dir = get_src_dir_path(__file__)
    data_dir = src_dir.parent / "data"

    # TODO: testing on Nov 11, 2020
    file_path = Spider().crawl(data_dir, date=datetime.date(year=2020, month=11, day=11))
    # file_path = Spider().crawl(data_dir)

    if file_path.endswith('.xlsx'):
        print("unhandled xlsx file!")

    elif file_path.endswith('.pdf'):
        tables = Wrangler.parse_pdf(file_path)
        breakpoint()
    else:
        raise ValueError(f"Unexpected file type: {file_path}")

    return None


if __name__ == "__main__":
    main()
