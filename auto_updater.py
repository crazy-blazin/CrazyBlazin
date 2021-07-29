import requests
from tqdm import tqdm
from zipfile import ZipFile
import os
import shutil
import subprocess
import time
from flask import Flask, render_template, url_for, request, jsonify
import pickle
from datetime import datetime, time
import numpy as np
import io
from PIL import Image
import matplotlib.pyplot as plt
import json
import jsonpickle
import random
from flask import Flask, render_template, url_for, request, Response, send_file
import http.client
from datetime import datetime, time
from matplotlib import image
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from pathlib import Path
import uuid
import glob
import shutil
import logging
from werkzeug.datastructures import FileStorage
from flask_restful import Resource, Api, reqparse
from werkzeug.utils import secure_filename
from fastapi import FastAPI
import requests
from tqdm import tqdm
from zipfile import ZipFile
import os
import shutil
import subprocess
import time


with open('version.txt', 'r') as f:
    version = float(f.read())

app = FastAPI()




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


async def check(zip_url):
    print('New version detected!')
    r = requests.get('http://localhost:5000/end')
    folder_name = extract_files(version, zip_url)
    time.sleep(6)
    subprocess.run(f"start python {version}/{folder_name}/even_newer/web/server.py", shell=True, check=True)
    time.sleep(5)
    subprocess.run(f"start python {version}/{folder_name}/even_newer/main.py", shell=True, check=True)



@app.get('/')
async def startupdate():
    with open('version.txt', 'r') as f:
        ver = float(f.read())
    zip_url, version = get_version()
    if version > ver:
        await check(zip_url)
        with open('version.txt', 'w') as f:
            f.write(str(version))
        return {'status': f'Version checked, new version {version} detected'}
    else:
        return {'status': 'Version checked, no new version!'}


# if __name__ == "__main__":
#     # socketio.run(app, debug=True)
#     app.run(debug=True, port=5100)