import os
import subprocess

import requests
from tqdm import tqdm
from stanfordnlp.utils.resources import unzip_ud_model

DEFAULT_MODEL_DIR = './stanford_resource'

def download(lang_name, resource_dir=DEFAULT_MODEL_DIR, should_unzip=True):
    if resource_dir is not None and os.path.exists(f"{resource_dir}/{lang_name}_models"):
        return
    download_dir = resource_dir
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    model_zip_file_name = lang_name + '_models.zip'
    download_url = 'http://nlp.stanford.edu/software/conll_2018/' + model_zip_file_name
    download_file_path = download_dir + '/' + model_zip_file_name

    # initiate download
    r = requests.get(download_url, stream=True)
    with open(download_file_path, 'wb') as f:
        file_size = int(r.headers.get('content-length'))
        default_chunk_size = 67108864
        with tqdm(total=file_size, unit='B', unit_scale=True) as pbar:
            for chunk in r.iter_content(chunk_size=default_chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    pbar.update(len(chunk))
    if should_unzip:
        unzip_ud_model(lang_name, download_file_path, download_dir)
    subprocess.call('rm ' + download_file_path, shell=True)


if __name__ == '__main__':
    download('en_ewt')
