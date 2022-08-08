import discord
from nbformat import read
import numpy as np
import os
import config
import h5py

k = os.getenv("DISCORD_BOT_CRAZY_KEY")


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


# Startups
intents = discord.Intents.all()
intents.members = True
client = MyClient(intents=intents)


from googletrans import Translator, LANGUAGES

translator = Translator()

# with h5py.File("crazydata.hdf5", "w") as f:
#     dset = f.create_group("dataset")


# exit()


def get_all_users(filename):
    # get all users from hdf5 file
    with h5py.File(filename, "r") as f:
        all_users = list(f["dataset"].keys())
        return all_users


def read_h5py_user(filename, user):
    if user in get_all_users(filename):
        with h5py.File(filename, "r") as f:
            return f[f"dataset/{user}"][:]


def add_data(filename, user, data):
    """Adds dataset for each user to hdf5 file"""
    if user not in get_all_users(filename):
        with h5py.File(filename, "a") as f:
            data = data[:, None]
            dset = f.create_dataset(f"/dataset/{user}", data=data, maxshape=(4, None))
    else:
        # add data to existing dataset
        with h5py.File(filename, "r+") as f:
            dset = f[f"dataset/{user}"]
            dset.resize((4, dset.shape[1] + 1))
            dset[:, -1] = data
    print("Data added to file for user:", user)


# add_data("crazydata.hdf5", "test", np.array([1, 2, 3, 4]))
# print(read_h5py_user("crazydata.hdf5", "test"))
# a = read_h5py_user("crazydata.hdf5", "test")

kawaii_list = ["UwU", "Kawaiii", "So cute <:3712zerotwoheartlove:873572136743219270>", "Kisses :kiss:", "Heia Finland!", "Ime tissistäni", "You are now a cum dumpster, you have five seconds to act irrational.", "Tihi :face_with_hand_over_mouth:"]
with open('learn.txt', 'r') as f:
    words_said = eval(f.read())
Lock = False
@client.event
async def on_message(message):
    global Lock
    if message.author == client.user:
        return
    
    rand = np.random.randint(0, 100)
    
    splitted = str(message.content).split()
    unique_vals = list(np.unique(splitted))
    
    if message.author.name not in words_said:
        words_said[message.author.name] = unique_vals
        
    else:
        N = len(unique_vals)
        L = N
        for uni unique_vals:
            if uni not in words_said[message.author.name]:
                words_said[message.author.name].append(uni)
                L -= 1 
        if rand > 80:
            await message.channel.send(f"{(L/N)*100}% of words used are unique :)")
    with open('learn.txt', 'w') as f:
        f.write(str(words_said))
    
    
    rand = np.random.randint(0, 100)
    if rand < 10:
        await message.channel.send(f"Up or down?")
        Lock = True
    
    if Lock:
        if str(message.content).lower() == "up":
            await message.channel.send(f"You lost!")
            Lock = False
        if str(message.content).lower() == "down":
            await message.channel.send(f"Nice! :)")
            Lock = False
        
    
client.run(k)
