import requests
from tqdm import tqdm
from zipfile import ZipFile
import os
import shutil
import subprocess
import time



url = 'https://api.github.com/repos/martinrovang/CrazyBlazin/releases'




def download_url(url, save_path, chunk_size=128**4):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size)):
            fd.write(chunk)



def extract_files(version, zip_url):
    download_url(zip_url, f'{version}.zip')
    with ZipFile(f'{version}.zip', 'r') as zipObj:
        folder_name = list(zipObj.namelist())[0].split('/')[0]
        # Extract all the contents of zip file in current directory
        zipObj.extractall(f'{version}')
        return folder_name

def get_version():
    r = requests.get(url)

    fetched = r.json()[0]

    zip_url = fetched['zipball_url']
    version = float(fetched['tag_name'])

    return zip_url, version



with open('version.txt', 'r') as f:
    ver = float(f.read())
zip_url, version = get_version()
if version > ver:
    print('New version detected!')
    folder_name = extract_files(version, zip_url)
    with open('version.txt', 'w') as f:
        f.write(str(version))
    time.sleep(5)
    subprocess.run(f"start python {version}/{folder_name}/even_newer/web/server.py", shell=True, check=True)
    time.sleep(6)
    subprocess.run(f"start python {version}/{folder_name}/even_newer/main.py", shell=True, check=True)
else:
    print('Version checked!')
