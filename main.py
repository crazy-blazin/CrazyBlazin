#!/usr/bin/env python
from asyncio.tasks import wait
import os
from sys import path
from discord import voice_client
import matplotlib.pyplot as plt
import numpy as np
import discord
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
import tools.painting as painting
import tools.animepaint as arcanetool
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import tools.activitydb as activitydb





# Globals
PAINT_LOCK = True
queue = []

# print(message.author.activity.name)

with open('../key.txt', 'r') as f:
    k = str(f.read())


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')


# Startups
intents = discord.Intents.all()
intents.members = True
client = MyClient(intents = intents)


db = activitydb.ActivityDB()


async def ticksystem():
    while True:
        await asyncio.sleep(10)
        global temp_status
        # database = read_db()
        global database
        remove_status = ["any problem can always be solved with generous amount's of big explosions and fire", "penis", "Sassy cunt, not rectifiable in any way."]
        temp_stats = {}
        members = client.get_all_members()
        for member in members:
            role_names = [role.name for role in member.roles]
            if 'Bots' not in role_names:
                if member.activity is not None:
                    if member.activity.name not in remove_status:
                        if member.activity.name not in temp_stats:
                            temp_stats[member.activity.name] = 1
                        else:
                            temp_stats[member.activity.name] += 1

        db.update_stats(temp_stats)
        db.plot_data()

async def timer():
    await client.wait_until_ready()
    await asyncio.sleep(4)

client.loop.create_task(ticksystem())



@client.event
async def on_message(message):
    global PAINT_LOCK
    global queue
    if message.author == client.user:
        return

    if str(message.channel.id) == '916636184707493958' or str(message.channel.id) == '734481490431443068':
        queue.append([str(message.content), message.channel])
        if len(queue) > 1:
            await queue[-1][1].send(f'Painting "{queue[-1][0]}" added to queue!')
        while len(queue) >= 1:
            if PAINT_LOCK:
                PAINT_LOCK = False
                PAINT_LOCK, queue = await painting.do_paint(queue)
            await asyncio.sleep(2)


    if message.content.startswith('!arcane'):
        str_split = message.content.split(' ')
        if len(str_split) > 2 or len(str_split) < 2:
            await message.channel.send(f'Too many or few arguments. Use !arcace <link to image>')
        else:
            await message.channel.send(f'Arcanifying....')
            path_imge = await arcanetool.arcanify(str_split[-1])
            if path_imge:
                await message.channel.send(file=discord.File(path_imge))
            else:
                await message.channel.send(f'You need to input link with correct format (link, .png, .jpg) and be an downloadable image!')
    
    if message.content.startswith('!activity'):
        await message.channel.send(file=discord.File('../activitydb.png'))

    
    if message.content.startswith('!restart'):
        subprocess.run("start killall.bat", shell=True, check=True)
        await message.channel.send(f'Restarting...')



client.run(k)