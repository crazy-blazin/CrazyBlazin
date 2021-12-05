#!/usr/bin/env python
from asyncio.tasks import wait
import os
from discord import voice_client
import matplotlib.pyplot as plt
import numpy as np
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import time
import threading
from discord.utils import get
from collections import Counter
import asyncio
from discord.ext import tasks
import datetime
import socketio
import uuid
import requests
from flask import jsonify
import logging
from datetime import date
import asyncio 
# OS modules
import os
import shutil
# Image modules
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw, ImageSequence
import subprocess
import audioread
import tempfile
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import pickle
from PIL import Image
import datetime
from config import *
import random
import glob
import card_game.cardsystem as cardsystem
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 




with open('../key.txt', 'r') as f:
    k = str(f.read())


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')




intents = discord.Intents.default()
intents.members = True
client = MyClient(intents = intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if message.content.startswith('!paint'):
        styles = {'Steampunk': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[9]/div/div/img', 'Fantasy': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[8]/div/div/img', 'Synthwave': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[11]/div/div/img', 'Pastel': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[5]/div/div/img', 'Mystical': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[1]/div/div/img', 'Ukiyoe': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[10]/div/div/img', 'Dark fantasy': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[3]/div/div/img', 'HD': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[6]/div/div/img', 'Festive': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div/div/img', 'Psychic': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[4]/div/div/img', 'Vibrant': '/html/body/div/div/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[7]/div/div/img'}
        str_split = message.content.split(' ')
        if len(str_split) < 2:
                await message.channel.send(f'Too many or few arguments. Use !paint <description/words>')
        else:
            str_split = str_split[1:]
            total_sentence = ''
            for word in str_split:
                total_sentence += word+' '
            await message.channel.send(f'Painting.... Please wait.')
            stl = random.choice(list(styles.items()))
            path_imge = cardsystem.do_card_regular(total_sentence, style = stl[1])
            await message.channel.send(file=discord.File(path_imge))
            time.sleep(2)
            files = glob.glob('C:/Users/foxx/Downloads/*')
            for f in files:
                os.remove(f)


client.run(k)