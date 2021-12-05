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
# import chromedriver_autoinstaller


# chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
#                                       # and if it doesn't exist, download it automatically,
#                                       # then add chromedriver to path

driver = webdriver.Chrome()
driver.get("https://app.wombo.art/")



def do_card(input_description = 'Grand Behemoth', type_ = 'BlackHole', style = '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/img'):

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



def do_card_regular(input_description = 'Grand Behemoth', style = '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/img'):

    # Equivalent Outcome! 
    time.sleep(2)
    id_box = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div[1]/input')

    # Send id information
    id_box.send_keys(input_description)
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
            id_box = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div/div[1]/div[2]/div/div[3]/div[1]/div/button').click()
            lock = False
        except:
            print('Still generating')

    # Reset
    input_description = input_description.replace(' ', '_')
    # path_out = f'C:/Users/Gimpe/Downloads/{input_description}_TradingCard.jpg'
    path_out = f'C:/Users/foxx/Downloads/{input_description}_TradingCard.jpg'
    print(os.path.exists(path_out))
    while not os.path.exists(path_out):
        print('not exist')
        time.sleep(1)

    time.sleep(3)   
    driver.refresh()
    
    return path_out
    # return f'C:/Users/Gimpe/Downloads/{input_description}_TradingCard.jpg'



    # Art styles;

    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[9]/div/div/img - Steampunk
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[8]/div/div/img - Fantasy
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[11]/div/div/img - Synthwave
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[5]/div/div/img - Pastel
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/img - Mystical
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[10]/div/div/img - Ukiyoe
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[3]/div/div/img - Dark fantasy
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[6]/div/div/img - HD
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/div/img - Festive
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[4]/div/div/img - Psychic
    # /html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[7]/div/div/img - Vibrant