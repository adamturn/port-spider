"""
Python 3.7
Author: Adam Turner <turner.adch@gmail.com>
"""

# standard library
import pathlib


def get_src_dir_path(file):
    """
    Args:
        file: __file__ object

    Returns: absolute pathlib Path to this project's /src directory.
    """
    src_dir_path = pathlib.Path(file).parent.absolute()
    if str(src_dir_path).endswith("src"):
        return src_dir_path
    else:
        raise ValueError(f"This file is not in the /src directory: {src_dir_path}")
