#!/usr/bin/python3

import glob
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import NamedTemporaryFile, TemporaryDirectory
from urllib.request import urlretrieve
from zipfile import ZipFile

ZIP_URL = 'https://www.itu.int/wftp3/Public/t/testsignal/SpeImage/T834/v2014_10/ITU-T_T.834(2014-10)_ConformanceSuite.zip'
ZIP_HASH = 'c066c5e24a212f3bb09eaf235cf21359754ffbb747d9fedc620e09629ca2a55d'
ZIP_ROOT = 'JXR_ConformanceSuite_2014'

SRCDIR = Path(__file__).parent
CASES_ZIP = Path('cases.zip')
CASES_DIR = Path('cases')
CASES_HASHES = SRCDIR / 'tiff-hashes.json'

def hash(path):
    digest = sha256()
    with open(path, 'rb') as fh:
        while True:
            buf = fh.read(1 << 20)
            if not buf:
                break
            digest.update(buf)
    return digest.hexdigest()


def download():
    if not CASES_ZIP.exists() or hash(CASES_ZIP) != ZIP_HASH:
        print('Fetching data set...')
        urlretrieve(ZIP_URL, CASES_ZIP)
        if hash(CASES_ZIP) != ZIP_HASH:
            raise Exception(f'Bad hash for {CASES_ZIP}')
    if not CASES_DIR.exists():
        with TemporaryDirectory(prefix='jxrtest-', dir='.') as dir:
            path = Path(dir)
            ZipFile(CASES_ZIP).extractall(path)
            os.rename(path / ZIP_ROOT, CASES_DIR)


def decode(decoder):
    with open(CASES_HASHES) as fh:
        hashes = json.load(fh)
    count = 0
    for path in sorted(CASES_DIR.rglob('*.jxr')):
        count += 1
        name = path.relative_to(CASES_DIR)
        if name.parent.name == 'Output_Color_Format_Advanced':
            continue
        with NamedTemporaryFile(prefix='jxrtest-', suffix='.tif') as f:
            subprocess.run([decoder, '-i', path, '-o', f.name], check=True)
            if hashes[str(name)] != hash(f.name):
                raise Exception(f'Hash mismatch for {name}')
    print(f'Decoded {count} cases.')


if __name__ == '__main__':
    download()
    decode(sys.argv[1])
