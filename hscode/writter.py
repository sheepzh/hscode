# -*- coding: utf-8 -*-
"""
    Write rows to files
"""
import time
import os


def check_directory(root_dir, write_to_latest=False):
    """
        Check whether the directories exist
    """
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    if write_to_latest:
        latest_dir = os.path.join(root_dir, 'latest')
        if not os.path.exists(latest_dir):
            os.makedirs(latest_dir)


def write(root_dir, chapter, rows, write_to_latest=False, include_outdated=False):
    """
        Write to the file
    """
    check_directory(root_dir, write_to_latest)
    curr_date = time.strftime('%Y%m%d_%H:%M', time.localtime())
    outdated_str = "including_outdated_" if include_outdated else ''
    file_name = 'hscode_' + outdated_str + chapter + '_' + curr_date + '.txt'

    rows_str = ["{}".format(row) for row in rows]
    content = "\r\n".join(rows_str)
    with open(os.path.join(root_dir, file_name), 'w') as file:
        file.writelines(content)

    if write_to_latest:
        latest_name = 'hscode_' + outdated_str + chapter + '.txt'
        with open(os.path.join(root_dir, 'latest', latest_name), 'w') as file:
            file.writelines(content)
