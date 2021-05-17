import bz2
import hashlib
import os
import sys
import urllib.parse
import urllib.request
from multiprocessing.pool import ThreadPool
from pathlib import Path

from toony import config
from toony.toontown import api

__MANIFEST_URL = 'https://cdn.toontownrewritten.com/content/patchmanifest.txt'
__PATCH_URL = 'https://download.toontownrewritten.com/patches/'


def update():
    if not (executable_path := config.get('Toontown', 'Path')):
        guess_path = os.path.join(Path.home(), 'Library/Application Support/Toontown Rewritten')
        if os.path.exists(guess_path):
            config.write('Toontown', 'Path', guess_path)
            executable_path = Path(guess_path)
        else:
            raise OSError('Toontown Rewritten path not defined or does not exist')

    if update_files := __get_update_files(Path(executable_path)):
        ThreadPool(len(update_files)).imap_unordered(__download, update_files)


def __get_update_files(executable_path: Path):
    files = []

    manifest = api.request(None, __MANIFEST_URL, format='json')
    for file in manifest.keys():
        if sys.platform not in manifest[file]['only']:
            continue

        if not (executable_path / file).exists():
            files.append((executable_path / file, urllib.parse.urljoin(__PATCH_URL, manifest[file]['dl'])))
            print(f'not {executable_path / file}.exists()')
            continue

        hash_alg = hashlib.sha1()
        hash_alg.update((executable_path / file).open('rb').read())
        if manifest[file]['hash'] != hash_alg.hexdigest():
            files.append((executable_path / file, urllib.parse.urljoin(__PATCH_URL, manifest[file]['dl'])))
            print(f'{manifest[file]["hash"]} != {hash_alg.hexdigest()}')

    return files


def __download(url):
    path, uri = url
    path = str(path) + '.bz2'
    urllib.request.urlretrieve(uri, path)
    __decompress(path)


def __decompress(bz2_path: str):
    with bz2.BZ2File(bz2_path, 'rb') as file, open(bz2_path[:-4], 'wb') as new_file:
        for data in iter(lambda: file.read(100 * 1024), b''):
            new_file.write(data)

    os.remove(bz2_path)
