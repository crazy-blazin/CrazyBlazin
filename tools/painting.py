
import random
import glob
import os
import asyncio
import discord
import tools.cardsystem as cardsystem


async def do_paint(queue):

    await queue[0][1].send(f'Painting "{queue[0][0]}"... Please wait. Currently {len(queue)-1} in queue.')
    # mystic = '11'
    # dark_fantasy = '10'
    # psychic = '9'
    # synthwave = '1'
    # vibrant = '6'
    # jule = "12"
    # steampunk = '4'
    # fantasy_art = '5'
    stl = random.choice([11, 10, 9, 1, 6, 4, 5])
    path_imge = await cardsystem.do_card_regular(queue[0][0], style = stl)
    await queue[0][1].send(file=discord.File(path_imge))
    await asyncio.sleep(2)
    files = glob.glob('C:/Users/foxx/Downloads/*')
    for f in files:
        os.remove(f)
    PAINT_LOCK = True
    queue.remove(queue[0])

    return PAINT_LOCK, queue