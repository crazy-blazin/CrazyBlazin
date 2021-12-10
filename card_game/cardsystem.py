from selenium import webdriver
import time
from asyncio.tasks import wait
import os
from discord import voice_client
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
from discord.ext import tasks

# Image modules
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw, ImageSequence
import pickle
from PIL import Image
import json
import requests
from requests.structures import CaseInsensitiveDict
# import chromedriver_autoinstaller


# chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
#                                       # and if it doesn't exist, download it automatically,
#                                       # then add chromedriver to path






def do_card(input_description = 'Grand Behemoth', type_ = 'BlackHole', style = '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/img'):
    driver = webdriver.Chrome()
    driver.get("https://app.wombo.art/")


    # Equivalent Outcome! 
    time.sleep(2)
    id_box = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/input')

    # Send id information
    id_box.send_keys(input_description+f' {type_}')
    time.sleep(1)

    # ART STYLE
    id_box = driver.find_element_by_xpath(style).click()
    time.sleep(2)

    id_box = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div/div[2]/div/button').click()

    lock = True
    while lock:
        try:
            time.sleep(15)
            id_box = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[1]/div[2]/div/div[1]/input')
            time.sleep(3)
            id_box.send_keys(input_description)
            time.sleep(3)

            id_box = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div[2]/div/div[2]').click()
            time.sleep(3)

            id_box = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[1]/div[2]/div/div[3]/div[1]/div/button').click()
            lock = False
        except:
            print('Still generating')

    input_description = input_description.replace(' ', '_')
    # path_out = f'C:/Users/Gimpe/Downloads/{input_description}_TradingCard.jpg'
    path_out = f'C:/Users/foxx/Downloads/{input_description}_TradingCard.jpg'
    while not os.path.exists(path_out):
        print('not exist')
        time.sleep(1)

    # Reset
    time.sleep(1)   
    driver.refresh()

    return path_out
    # return f'C:/Users/Gimpe/Downloads/{input_description}_TradingCard.jpg'


def grab_keys():
    with open('../apikeys.txt', 'r') as f:
        keys = eval(str(f.read()))
    return keys

async def do_card_regular(input_description = 'Grand Behemoth', style = 5):

    to_send = json.dumps({"input_spec":{"prompt":input_description,"style":style,"display_freq":10}})
    headers = CaseInsensitiveDict()
    keys_ = grab_keys()
    googapi = keys_['googapi']
    paintlink = keys_['paintlink']
    response_token = requests.post(googapi, data = {"returnSecureToken":'true'})
    idToken = response_token.json()['idToken']

    headers["Authorization"] = "bearer " + idToken
    response_painter = requests.post(paintlink, headers = headers, data = json.dumps({"premium":"false"}))
    id = response_painter.json()['id']
    response_put = requests.put(f'{paintlink}{id}', headers = headers, data = to_send)

    await asyncio.sleep(3)
    while True:
        response = requests.get(f'{paintlink}{id}', headers = headers)
        img_list = len(response.json()['photo_url_list'])
        await asyncio.sleep(5)
        response = requests.get(f'{paintlink}{id}', headers = headers)
        img_list2 = len(response.json()['photo_url_list'])
        print(img_list2, img_list)
        if img_list2 == img_list:
            photo = response.json()['photo_url_list'][-1]
            path_out = f'C:/Users/foxx/Downloads/output.jpg'
            # requests download image from url and save it to path
            with open(path_out, 'wb') as f:
                f.write(requests.get(photo).content)
            break


    timeout_counter = 0
    while not os.path.exists(path_out):
        print('not exist')
        await asyncio.sleep(1)
        timeout_counter += 1
        if timeout_counter > 70:
            path_out = 'error.jpg'
            break
    
    return path_out

