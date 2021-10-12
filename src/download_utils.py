import hashlib
import os
import re
from pathlib import Path

import requests
from icecream import ic


def _get_md5sum_local_file(f_path):
    hash = hashlib.md5()
    try:
        if os.path.isfile(f_path):
            with open(f_path, "rb") as lf:
                hash.update(lf.read())
    finally:
        return hash.hexdigest()


def _get_lastest_md5sum(md5sum_url):
    response = requests.get(md5sum_url)
    # We are only interested in the 32 char string, not the file name
    match = re.search("^([0-9a-f]{32})[ ]{2}.*$", response.text)
    return match.group(1)


def _download_file(download_url, target_path):
    if not Path.exists(Path(target_path).parent):
        Path.mkdir(Path(target_path).parent, parents=True)

    chunk_size = 1024
    response = requests.get(download_url)
    with open(target_path, mode="wb") as fb:
        for chunk in response.iter_content(chunk_size=chunk_size):
            fb.write(chunk)


def download_latest_file(download_url, target_filename, md5sum_url=None):
    ic.enable()
    # target_path = f"downloads/{target_filename}"
    target_path = target_filename
    ic(target_path)
    if md5sum_url:
        if _get_md5sum_local_file(target_path) != _get_lastest_md5sum(md5sum_url):
            ic("Remote files is different to localfile, downloading update.")
            _download_file(download_url, target_path)
    else:
        if not os.path.exists(target_path):
            ic("local file does not exist, downloading new file.")
            _download_file(download_url, target_path)
