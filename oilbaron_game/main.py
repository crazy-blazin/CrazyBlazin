import discord
from nbformat import read
import numpy as np
import os
import config
import h5py
import qrcode
import uuid
import time

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
    
def save_data(filename, data):
    with open(filename, 'w') as f:
        f.write(str(data))
        
        
def load_data(filename):
    with open(filename, 'r') as f:
        return eval(f.read())
      
      
oildata = load_data('oilbarrels.txt')
words_said = load_data('learn.txt')

# img = qrcode.make("http://192.168.1.234:5000/someid")
# type(img)  # qrcode.image.pil.PilImage
# img.save("some_file.png")

@client.event
async def on_message(message):
    global words_said
    global oildata
    if message.author == client.user:
        return
    
    users = load_data('users.txt')
    if message.author.name not in users:
        users[message.author.name] = 1
    
    if message.content.startswith('!change'):
        what_we_have = load_data("whatwehave.txt")
        id = str(uuid.uuid1())[:5]
        #img = qrcode.make(f"https://service-9703.something.gg/{id}")
        what_we_have[id] = message.author.name
        save_data("whatwehave.txt", what_we_have)
        print(what_we_have)
        #img.save("some_file.png")
        time.sleep(0.5)
        #await message.channel.send(file=discord.File('some_file.png'))
        await message.channel.send(f"https://service-9703.something.gg/{id}")
    
    
    rand = np.random.randint(0, 100)
    if rand > 90:
        country_chosen = np.random.choice(list(oildata["Country"].keys()))
        await message.channel.send(f"You diverted {int(users[message.author.name])} oil barrel :fuelpump: to {country_chosen} from your pipeline.")
        oildata['Country'][country_chosen]['oilstorage'] += int(users[message.author.name])
        save_data('oilbarrels.txt', oildata)
    
    if message.content.startswith('!stats'):
        for main_stat in oildata:
            if main_stat == "Country":
                for country in oildata[main_stat]:
                    embedVar = discord.Embed(title=country, description="The current portofolio of country",color=0x00ff00)
                    for data in oildata[main_stat][country]:
                        embedVar.add_field(name="Oil storage:", value=f":fuelpump: {oildata[main_stat][country][data]}", inline=False)
        await message.channel.send(embed=embedVar)
      
        
        
    
                
            
               
client.run(k)
