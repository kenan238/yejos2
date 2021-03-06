from inspect import indentsize
from itertools import permutations
from typing import Text
import discord
from discord import channel
from discord import integrations
from discord.client import Client
from discord.embeds import Embed
from discord.ext import commands
import random
rnd = random
import aiohttp
import os
import asyncio as asio
import json
import time
from discord.ext.commands import cooldown, BucketType
import atexit
import asyncio
import sys
from yeg_os import YEGOS

intents = discord.Intents.default()
intents.members = True
client_ = discord.Client(intents=intents)

client = commands.Bot(command_prefix=">", help_command=None)
numixAccFile = "SECRET_FOLDER/numixAccs.json" # path for the accounts db
utilities = ["PHONE_UTILITY", "CAN_BE_EATEN", "CAN_FISH", "CAN_SHOOT_PEOPLE", "CAN_SHOOT_DEMONS", "COMPUTER", "OS"] # item utilities
computer_types = ["laptop", "gaming_laptop"]
items_not_in_shop = ["demon_destroyer"] # items hidden in shop
sold_items_by_users = [] # sold items by users
sold_items_by_users_file = "SECRET_FOLDER/solditems.json"
accStructure = { # how an account should be in the db
    "coins": 0,
    "inventory": [],
    "strength": 0,
    "stamina": 0,
    "job": "",
    "laptop_os": "none",
    "laptop_specs_cpu": "none",
    "laptop_specs_gpu": "none",
    "laptop_specs_ram": "none",
    "laptop_specs_storage_media": "none",
    "laptop_disk": {},
}
jobs = {
    "shop": [5, 20],
}
foods = {
    #"FOODNAME": STAMINA_AMT
    "apple": 1,
    "fish":  2,
    "le_fishe_au_chocolat": 5
}
items = { # list of items
    "phone": {
        "utility": ["PHONE_UTILITY"],
        "price": 20
    },
    "fishing_rod": {
        "utility": ["CAN_FISH"],
        "price": 10
    },
    "apple": {
        "utility": ["CAN_BE_EATEN"],
        "price": 2
    },
    "fish": {
        "utility": ["CAN_BE_EATEN"],
        "price": 5
    },
    "shotgun": {
        "utility": ["CAN_SHOOT_PEOPLE"],
        "price": 16
    },
    "le_fishe_au_chocolat": {
        "utility": ["CAN_BE_EATEN"],
        "price": 4
    },
    "demon_destroyer": {
        "utility": ["CAN_SHOOT_DEMONS"],
        "price": 21,
    },
    "laptop": {
        "utility": ["COMPUTER"],
        "price": 100,
    },
    "gaming_laptop": {
        "utility": ["COMPUTER"],
        "price": 100,
    },
    "YEG_OS": {
        "utility": ["OS"],
        "price": 6
    },
}

async def async_on_exit():
    channel = client.get_channel(899210171321028649)
    embed = get_status_embed(1, False)
    await channel.purge(limit=5)
    await channel.send(embed = embed)
    await client.change_presence(status=discord.Status.offline)

# def on_exit():
#     asyncio.run(async_on_exit())

# atexit.register(on_exit)

def get_status_embed(status, maintenance):
    embed = discord.Embed(
        title = f'Status',
        description = 'what da bot doin?',
        color = discord.Color.purple()
    )
    msg = None
    if status == 0:
        status = ":green_circle: Online"
    elif status == 1:
        status = ":red_circle: Offline"

    if not maintenance:
        maintenance = ":no_entry_sign:"
    else:
        maintenance = ":white_check_mark:"

    embed.add_field(name="Status", value=f"{status}")
    embed.add_field(name="Maintenance", value=f"{maintenance}")  
    return embed

@client.event
async def on_ready():
    print("Logged in.")
    await client.change_presence(status=discord.Status.online)

    # Display status
    channel = client.get_channel(899210171321028649)
    embed = get_status_embed(0, False)
    await channel.purge(limit=5)
    await channel.send(embed = embed)

    with open(numixAccFile, "r+") as f:
        if f.read() == "": # fill db if empty
            f.write(json.dumps({"database": {}}))
    with open(sold_items_by_users_file, "r+") as f:
        if f.read() == "": # fill db if empty
            f.write(json.dumps({"database": {}}))
        

# async def do_request(url):
#     print(f"do_request called with url={url}")
#     async with aiohttp.ClientSession().get(url=url) as data:
#         return data

def max_idx(l):
    idx, biggest = (0, 0)
    cIdx = 0
    for elem in l: # loop thru elements
        if elem > biggest: # simple sorting
            biggest = elem
            idx = cIdx
    return idx
def getAcc(id): # get the account by id
    file = json.load(open(numixAccFile, "r"))["database"]
    if id in file:
        return file[id]
    return "USER_NOT_FOUND"
def createAcc(id): # create an account by id
    struct = accStructure
    file = json.load(open(numixAccFile, "r"))["database"]
    file[id] = struct
    with open(numixAccFile, "w") as f:
        f.write(json.dumps({
            "database": file
            }))
def readAccsFile(): # read accounts db file
    return json.load(open(numixAccFile, "r"))["database"]
def getItem(name): # get item
    if item not in name:
        return "ITEM_NOT_FOUND"
    return items[name]
def saveChangesToAcc(id, changes): # save changes to account
    file = json.load(open(numixAccFile, "r"))["database"]
    file[id] = changes
    with open(numixAccFile, "w") as f:
        f.write(json.dumps({
            "database": file
            }))
def writeToJson(file, data):
     with open(file, "w") as f:
        f.write(json.dumps(data))
def sellItem(user, item, price):
    file = json.load(open(sold_items_by_users_file, "r"))
    file[random.choice("qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM") * 20] = {"item": item, "user": user, "price": price}
    writeToJson(sold_items_by_users_file, file)
def getSoldItems():
    return json.load(open(sold_items_by_users_file, "r"))
def removeSoldItem(userid, itemname):
    file = getSoldItems()
    file_loop = file.copy()
    for item in file_loop:
        if file_loop[item]["user"] == userid and file_loop[item]["item"] == itemname:
            del file[item]
    writeToJson(sold_items_by_users_file, file)



#######
#OSES##
#######

class YEGOS_setup:
    def write_to_disk(self, disk, path, data):
        if type (data) == str:
            data = f"\"{data}\""
        spath = ""
        for p in path.split("/"):
            spath += f"['{p}']"
        try:
            exec(f"disk{spath} = {data}")
            return disk
        except KeyError:
            return None

    def peek_at_disk(self, disk, path):
        currentPoint = disk
        path = path.split("/")
        try:
            for key in path:
                currentPoint = currentPoint[key]
            return currentPoint
        except KeyError:
            return None



    def __init__(self):
        self.cur_user = None
        self.logo = """
   ..::::::::.
  :::::::::::::
 /. `:::::::::::
o__,_::::::::::'
        """
    async def ask (self, client, ctx):
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        return msg



    async def setup (self, client, ctx, acc):
        if self.peek_at_disk (acc["laptop_disk"], "yeg_os/setup/installed") == None:
            await ctx.send(f"```{self.logo}```")
            await ctx.send("`Welcome to YEG OS Setup!`")
            time.sleep(0.1)
            await ctx.send("`Enter your name please (20 seconds):`")
            name = await self.ask(client, ctx)
            name = name.content
            self.write_to_disk (acc["laptop_disk"], "yeg_os", {})
            self.write_to_disk (acc["laptop_disk"], "yeg_os/setup", {})
            self.write_to_disk (acc["laptop_disk"], "yeg_os/setup/installed", True)
            self.write_to_disk (acc["laptop_disk"], "yeg_os/rootfs", None)
            await ctx.send("`Current network: YEJOS_NET`")
            time.sleep(0.1)
            await ctx.send("Setup done!")
            saveChangesToAcc(str(ctx.message.author.id), acc)
        else:
            await ctx.send("`Looks like a installation of YEG_OS is already present on the disk.`")
            await ctx.send("`Would you like to format the disk? [y/n]` (20 seconds)")
            yesno = await self.ask(client, ctx)
            yesno = yesno.content
            if yesno == "y":
                acc["laptop_disk"] = {}
                await ctx.send("`Your disk has been wiped out! Reboot for setup.`")
            if yesno == "n":
                await ctx.send("`Your disk is intact.`")


async def YEG_OS_(client, ctx, acc):
    await YEGOS_setup().setup(client, ctx, acc)
    saveChangesToAcc(ctx.message.author.id, await YEGOS().boot(client, ctx, acc))

#######




# Commands
# Help command

@client.command(name= 'help')
async def help(ctx): # help command
    embed = discord.Embed(
        title = 'Help',
        description = 'Help page',
        color = discord.Color.green()
    )
    embed.add_field(name= 'General', value='`hedgehog`')
    embed.add_field(name= 'Fun', value= '`meme` ' '`poll` ' '`ping` `say` `spoopy` `stats` `transfer_coins` `shop` `buy` `jackpot` `use_item` `apply_for_job` `work` `jobs_list` `buy_item_user` `leaderboard`', inline=False)
    embed.add_field(name= 'Moderation', value= '`ban` ' '`kick` ' '`lockdown` ' '`unlock`', inline=False)
    embed.set_image(url= 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fcute-hedgehog-bath.jpg&f=1&nofb=1')
    embed.set_thumbnail(url= 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fhedgehog-rainbow.jpg&f=1&nofb=1')
    await ctx.reply(embed=embed)



# Lockdown and unlock commands

# Lockdown command

@client.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.reply(ctx.channel.mention + " is in lockdown...")

# unlock command

@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.reply(ctx.channel.mention + " has been successfully unlocked!")



# Ban and Kick commands

# Ban command

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)

# Kick command

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    if "886937487912620032" in [y.id for y in member.roles]:
      try:
          await member.send("You have been kicked from the server.")
      except:
          await ctx.reply("The member has their DMS closed.")
      await member.kick(reason=reason)
    else:
        await ctx.reply('You do not have the permissions required.')

# Mute command

@client.command()
async def mute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="muted") # get muted role
    guild = ctx.guild
    if role not in guild.roles: # if muted role doesn't exist
        perms = discord.Permissions(send_message=False, speak=False) # make one
        await guild.create_role(name="muted", permutations=perms)
        await member.add_roles(role)
        await ctx.reply(f"{member} was muted.") # then mute
    else:
        await member.add_roles(role)
        await ctx.reply(f"{member} was muted.")

# Hedgehogs commands

@client.command()
async def hedgehog(ctx): # broken
    async with aiohttp.ClientSession().get(url="https://www.reddit.com/r/Hedgehogs/.json") as data:
        if data.status == 200:
            hedgehogs = await data.json(content_type=None)
            embed = discord.Embed(
                color = discord.Color.purple()
            )
            embed.set_image(url=hedgehogs["data"]["children"][random.randint(0, 25)]["data"]["url"]),
            embed.set_footer(text=f"Powered by r/Hedgehogs | Hedgehog requested by {ctx.author}"),
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("reddit sent not good status: " + str(data.status))



# Fun

# Memes commands

@client.command()
async def meme(ctx): # broken
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/memes/.json") as r:
           memes = await r.json(content_type=None)
           embed = discord.Embed(
               color = discord.Color.purple()
           )
           embed.set_image(url=memes["data"]["children"][random.randint(0, 25)]["data"]["url"]),
           embed.set_footer(text=f"Powered by r/memes | Meme requested by {ctx.author}"),
           await ctx.reply(embed=embed)



# Ping and pong

@client.command()
async def ping(ctx):
    await ctx.reply("pong, -0 ms") # le funne ping



# Poll command

@client.command()
async def poll(ctx,*,message): # poll
    emb=discord.Embed(title=" POLL ????", description=f"{message}", text=f"Poll requested by {ctx.author}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('??????')
    await msg.add_reaction('??????')



# Errors

@client.event
async def on_command_error(ctx,error): # command handling
    if isinstance(error,commands.MissingPermissions): # for missing perms
        await ctx.reply("You don't have permissions to do that.")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument): # missing arguments
        await ctx.reply("Please enter the required argument.")
        await ctx.message.delete()
    elif isinstance(error,commands.MemberNotFound): # unexistant member
        await ctx.reply("This member do not exist.")
        await ctx.message.delete()
    elif isinstance(error, commands.CommandOnCooldown): # cooldown handling
            em = discord.Embed(title=f"take a chill pill bruv",description=f"Spam isn't cool fam. Try again in {error.retry_after:.2f}s. This command is on cooldown.", color=discord.Color.red())
            await ctx.reply(embed=em)
    else:
        raise error

# Say command
@client.command()
async def say(ctx, *, msg): # say command
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.reply(msg)

# spoopy

@client.command()
async def spoopy(ctx): # SPOOPY SCARY SKELETON
    await ctx.reply("https://cdn.discordapp.com/attachments/885888076260454461/897169777045430303/unknown.png")

# Numix Acc stats

@client.command()
async def stats(ctx, user: discord.Member = None): # stats command
    if user == None:
        user = ctx.message.author
    account = getAcc(str(user.id)) # get user
    if account == "USER_NOT_FOUND":
        await ctx.reply("I can't find your numix account, ima create one real quick...")
        createAcc(str(user.id))
    embed = discord.Embed( # make embed
        title = f'Account Stats - {user.name}',
        description = 'Stat page',
        color = discord.Color.green()
    )
    formattedInv = ""
    inv = account["inventory"]
    for item in inv: # inventory list to string
        formattedInv += f"{item}\n"
    embed.add_field(name= 'Coins', value=f'`{account["coins"]}`') # add fiels
    embed.add_field(name= 'Inventory', value=f'`{formattedInv}`')
    embed.add_field(name= 'Strength', value=f'`{account["strength"]}`')
    embed.add_field(name= 'Stamina', value=f'`{account["stamina"]}`')
    embed.add_field(name= 'Job', value=f'`{account["job"]}`')
    embed.set_thumbnail(url= 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fhedgehog-rainbow.jpg&f=1&nofb=1') # set le funne hedgehog image
    await ctx.reply(embed = embed) # send

# Fix database
@client.command()
async def fixDb(ctx): # fix db
    msg = await ctx.reply("Beggining to fix bad stuff inside db...")
    db = json.load(open(numixAccFile, "r"))["database"]
    fixedTotal = 0
    for key in db: # loop thru keys
        acc = db[key]
        for s in accStructure: # fix missing keys
            if s not in acc:
                acc[s] = accStructure[s]
                fixedTotal += 1
                await msg.edit(content=f"Fixed {fixedTotal} bad stuff, the {s} key was missing. Continuing...")
                print(f"Fixed {fixedTotal} bad stuff, the {s} key was missing. Continuing...")
        acc2 = acc.copy()
        for aitm in acc: # fix invalid keys
            if aitm not in accStructure:
                del acc2[aitm]
                fixedTotal += 1
                await msg.edit(content=f"Fixed {fixedTotal} bad stuff, the {aitm} key was an invalid key. Continuing...")
                print(f"Fixed {fixedTotal} bad stuff, the {aitm} key was an invalid key. Continuing...")
        if acc["job"] not in jobs and acc["job"] != "":
            acc["job"] = accStructure["job"]
            await msg.edit(content=f"Fixed {fixedTotal} bad stuff, <@!{key}>'s account had an invalid value as a job (sry for ping), Continuing...")
            print(f"Fixed {fixedTotal} bad stuff, <@!{key}>'s account had an invalid value as a job (sry for ping), Continuing...")
        if int(acc["strength"]) < 0:
            await msg.edit(f"Fixed {fixedTotal} bad stuff, k k ik this is funny but <@!{key}>'s account had negative strength ultimate stick (sry for ping)")

        db[key] = acc2.copy()
        del acc2
    with open(numixAccFile, "w") as f:
        f.write(json.dumps(db)) # write to file
    await ctx.reply(f"End. Fixed {fixedTotal} bad stuff.")

# Shop
@client.command()
async def shop(ctx):
    embed = discord.Embed(
        title = f'Shop',
        description = 'let\'s buy stuff',
        color = discord.Color.red()
    )
    for item in items: # loop thru items and add fiels
       if item not in items_not_in_shop:
           embed.add_field(name= f"*Name*: {item}", value=f'`Cost: {items[item]["price"]} NumixCoins`')
    sitems = getSoldItems()
    for item in sitems:
        embed.add_field(name= f"*Name*: {sitems[item]['item']}", value=f'`Cost: {sitems[item]["price"]} NumixCoins **SOLD BY `<@!{sitems[item]["user"]}> `USER_ID: {sitems[item]["user"]}**`')
    embed.set_thumbnail(url= 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fhedgehog-rainbow.jpg&f=1&nofb=1')
    await ctx.reply(embed = embed)

# Buy
@commands.cooldown(2, 5, commands.BucketType.user)
@client.command()
async def buy(ctx, itemname): # buy command
    if itemname not in items:
        await ctx.reply("that item doesnt exist bruh")
    account = getAcc(str(ctx.message.author.id))
    if itemname in computer_types and itemname in account["inventory"]:
        await ctx.reply("you can only have one pc")
        return
    if account == "USER_NOT_FOUND":
        await ctx.reply("use `>stats` to create a numix account because you don't have one")
    else:
        if account["coins"] < items[itemname]["price"]: # if too poor
            await ctx.reply("you don't have enough money to buy this item.")
        else:
            account["coins"] -= items[itemname]["price"] # remove price from coins
            account["inventory"].append(itemname) # add item to inv
            if itemname == "laptop":
                account["laptop_specs_cpu"] = "YEtel i5 5th gen"
                account["laptop_specs_gpu"] = "YEtel UHD Graphics"
                account["laptop_specs_ram"] = "10gb"
                account["laptop_specs_storage_media"] = "500gb hdd"
            if itemname == "gaming_laptop":
                account["laptop_specs_cpu"] = "YEtel i7 10th gen"
                account["laptop_specs_gpu"] = "GTS 1060 Ti"
                account["laptop_specs_ram"] = "15gb"
                account["laptop_specs_storage_media"] = "1tb ssd"
            
            await ctx.reply(f"You bought `{itemname}`, do `>stats` to see the item in your inventory")
    saveChangesToAcc(str(ctx.message.author.id), account) # write everything in

# Buy item sold by user
@client.command()
async def buy_item_user(ctx, userid = None, itemname = None):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.reply("use `>stats` to create a numix account because you don't have one")
    if userid == None or itemname == None:
        await ctx.reply("use the command as following: `>buy_item_user USER_ID NAME_OF_SOLD_ITEM`")
    sitems = getSoldItems()
    boughtSomething = False
    if sitems != {}:
        for item in sitems:
            name = sitems[item]["item"]
            user = sitems[item]["user"]
            price = int(sitems[item]["price"])
            
            if name == itemname and user == userid:
                removeSoldItem(user, name)
                acc["inventory"].append(name)
                if acc["coins"] < price:
                    await ctx.reply("you don't have enough money to buy this")
                    return
                acc["coins"] -= price
                seller_acc = getAcc(userid)
                seller_acc["coins"] += price
                
                saveChangesToAcc(str(ctx.message.author.id), acc)
                saveChangesToAcc(userid                    , seller_acc)
                boughtSomething = True
                await ctx.reply(f"You bought from {userid}")
    if not boughtSomething:
        await ctx.reply("this user hasn't sold anything")
        
# Transfer Coins
@client.command()
async def transfer_coins(ctx, to: discord.Member = None, amt: int = None): # transfer coins
    if to == None:
        await ctx.reply("I need to transfer some coins to someone, can't transfer to no one")
        return
    if amt == None:
        await ctx.reply("how much do you want to send? i cant read your mind")
        return
    user  = getAcc(str(ctx.message.author.id))
    to_   = getAcc(str(to.id))
    if user == "USER_NOT_FOUND": # can't find user 
        await ctx.reply("can't find your account, do `>stats` so i can create one for u")
        return
    if to_  == "USER_NOT_FOUND": # can't find user 2.0
        await ctx.reply(f"can't find the account of {to.name}, make them do `>stats` so i will make them an account")
        return
    if user["coins"] < amt: # not enough coins
        await ctx.reply("you don't have enough coins")
        return
    user["coins"] -= amt # do transfer
    to_ ["coins"] += amt
    saveChangesToAcc(str(ctx.message.author.id), user) # save
    saveChangesToAcc(str(to.id)                , to_ )
    await ctx.reply(f"Transfered {amt} coin(s) to {to.name}")

# Jackpot
@commands.cooldown(1, 30, commands.BucketType.user)
@client.command()
async def jackpot(ctx): # jackpot
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.reply("can't find your account, do `>stats`")
        return 
    await ctx.reply("???? Rolling...")
    rolls = ["????", "????", "????", "????", "????"] # emojis
    rolls_cost = {
        "????": 2, 
        "????": 6, 
        "????": 20, 
        "????": 40, 
        "????": 60
    } # how much luck every emoji is
    rolled = [
        rnd.choice(rolls), 
        rnd.choice(rolls), 
        rnd.choice(rolls)
    ] # roll
    await ctx.reply(f"{rolled[0]} `?` `?`") # display roll
    time.sleep(0.1)
    await ctx.reply(f"{rolled[0]} {rolled[1]} `?`")
    time.sleep(0.1)
    await ctx.reply(f"{rolled[0]} {rolled[1]} {rolled[2]}")
    
    
    amt = 0
    
    luck = rolls_cost[rolled[0]] + rolls_cost[rolled[1]] + rolls_cost[rolled[2]]
    chose = False
    # some questionable code for giving amounts
    if luck <= 8 and not chose:
        amt = 2
        chose = True
    if luck <= 12 and not chose:
        amt = 10
        chose = True
    if luck <= 15 and not chose:
        amt = 13
        chose = True
    if luck <= 29 and not chose:
        amt = 35
        chose = True
    if luck <= 80 and not chose:
        amt = 40
        chose = True
    if luck <= 100 and not chose:
        amt = 59
        chose = True
    if luck <= 180 and not chose:
        amt = 100
        chose = True
    
    acc["coins"] += amt # add coins
    saveChangesToAcc(str(ctx.message.author.id), acc) # save
    await ctx.reply(f"You won {amt} coins")

# Use item
@commands.cooldown(2, 6, commands.BucketType.user)
@client.command()
async def use_item(ctx, itemname, phone_arg: discord.Member = None): # use item
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND": # if user does not exist
        await ctx.reply("can't find your account, do `>stats`")
        return 
    if itemname not in acc["inventory"]: # if item is not in inventory
        await ctx.reply("you don't have this item")
        return
    utility = items[itemname]["utility"]
    for util in utility: # handle error
        if util not in utilities:
            await ctx.reply(f"Internal Error: {util} is not a valid utility")
            return
    await ctx.reply(f"Using {itemname}.")
    for util in utility: # start using
        if util == "OS":
            foundPC = False
            for t in computer_types:
                if t in acc["inventory"]:
                    foundPC = True
            if not foundPC:
                await ctx.reply("you do not have a computer, do `>buy laptop`")
                return
            for item in acc["inventory"]:
                if item in computer_types:
                    print(itemname) # debugging
                    acc["laptop_os"] = itemname
                    break
            saveChangesToAcc(str(ctx.message.author.id), acc)
        if util == "PHONE_UTILITY":
            if phone_arg == None:
                await ctx.reply("Provided the required argument: `>use_item itemname PERSON_TO_TEXT`")
                return
            dm = await phone_arg.create_dm()
            await ctx.reply("What message do you want to send? (You have 20 seconds)")
            msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            await dm.send(f"**Sent from {ctx.message.author.name}'s phone: ** {msg.content}") # send message
        if util == "CAN_BE_EATEN":
            if itemname not in foods:
                await ctx.reply(f"Internal error: {itemname} has utility 'CAN_BE_EATEN' but is not marked in the 'foods' list.")
                return
            acc["stamina"] += foods[itemname] # eat
            acc["inventory"].remove(itemname)
            saveChangesToAcc(str(ctx.message.author.id), acc)
            await ctx.reply(f"you ate {itemname} and got {foods[itemname]} stamina")
        if util == "CAN_FISH": # fish 
            fished = rnd.randint(0, 5)
            if fished == 5:
                await ctx.reply("Got a fish!")
                acc["inventory"].append("fish")
                saveChangesToAcc(str(ctx.message.author.id), acc)
            else:
                await ctx.reply("no fish ;-;")
        if util == "CAN_SHOOT_PEOPLE": # o-o
            if phone_arg == None:
                await ctx.reply("Use this command as `>use_item shotgun PING_THE_PERSON_YOU_WANT_TO_SHOOT`") 
            if phone_arg != None:
                slost = rnd.randint(1, 8)
                l = getAcc(str(phone_arg.id))
                if l == "USER_NOT_FOUND":
                    await ctx.reply("can't find the other user's numix account, make them do `>stats` so i will make them one")
                    return
                if l["strength"] < slost:
                    await ctx.reply("they got too low strength, they wont get negative strength")
                    return
                l["strength"] -= slost
                saveChangesToAcc(str(phone_arg.id), l)
                await ctx.reply(f"Shot {phone_arg.name}, they lost {slost} strength")
        if util == "COMPUTER":
            if acc["laptop_os"] == "none":
                await ctx.reply("You need a copy of an OS.")
                return
            await ctx.send("Booting....")
            if acc["laptop_os"] == "YEG_OS":
                await YEG_OS_(client, ctx, acc)
        if util == "CAN_SHOOT_DEMONS": # o-o
            acc["coins"] += 9
            saveChangesToAcc(str(ctx.message.author.id), acc)
            await ctx.reply("KILLED A DEMON +9 NUMIX COIN FOR HELPING SUSCIETY.")
# Do sports
@client.command()
async def do_sports(ctx, lvl: str = None): # do sports
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.reply("can't find your account, do `>stats`")
        return
    if lvl == None:
        await ctx.reply("What level of sports do you want to do (easy, medium, hard)? (20 seconds to answer)")
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content not in ["easy", "medium", "hard"]: # check if valid level
            await ctx.reply("bruh, that is not a sport level")
            return
        level = msg.content
    else:
        if lvl not in ["easy", "medium", "hard"]:
            await ctx.reply("bruh, that is not a sport level")
            return
        level = lvl
    if level == "easy":
        if acc["stamina"] < 3: # check stamina
            await ctx.reply("not enough stamina, need 3 stamina")
            return
        stoadd = rnd.randint(1, 3)
        acc["strength"] += stoadd # add strength
        acc["stamina"] -= 3 # remove stamina
        saveChangesToAcc(str(ctx.message.author.id), acc)
        await ctx.reply(f"you did an easy session of sports, +{stoadd} strength, -3 stamina")
        return
    if level == "medium":
        if acc["stamina"] < 5:
            await ctx.reply("not enough stamina, need 5 stamina")
            return
        stoadd = rnd.randint(5, 8)
        acc["strength"] += stoadd
        acc["stamina"] -= 5
        saveChangesToAcc(str(ctx.message.author.id), acc)
        await ctx.reply(f"you did a medium session of sports, +{stoadd} strength, -5 stamina")
        return
    if level == "hard":
        if acc["stamina"] < 8:
            await ctx.reply("not enough stamina, need 8 stamina")
            return
        stoadd = rnd.randint(9, 14)
        acc["strength"] += stoadd
        acc["stamina"] -= 8
        saveChangesToAcc(str(ctx.message.author.id), acc)
        await ctx.reply(f"you did a hard session of sports, +{stoadd} strength, -8 stamina")
        return

# leaderboard
@client.command()
async def leaderboard(ctx, depth_arg = None):
    embed = discord.Embed(
        title = f'Leaderboard',
        description = 'best users',
        color = discord.Color.red()
    )
    accounts = [] # accounts sorted from best to worse (LEN = DEPTH)
    depth = 4
    if depth_arg != None:
        depth = int(depth_arg)
    costs = {} # accounts with cost
    accs = readAccsFile()
    cIdx = 0

    for acc in accs: # fill in costs
        if cIdx >= depth:
            break
        cost = accs[acc]["strength"] + accs[acc]["stamina"] + accs[acc]["coins"]
        costs[int(cost)] = (acc, accs[acc].copy())
        cIdx += 1

    for acc in sorted(costs.keys()): # sort
        accounts.append((costs[acc], acc))
    
    accounts.reverse()

    bestUser = False
    for i in range(depth): # show
        add = ""
        if not bestUser:
            add = "????"
            bestUser = True
        acc_ = [s for s in accounts[i]]
        acc__ = acc_[0]
        embed.add_field(name= f"{add}{acc__[0]}", value=f'(**<@!{acc__[0]}>**) Coins: {acc__[1]["coins"]} | Stamina: {acc__[1]["stamina"]} | Strength: {acc__[1]["strength"]}')
    
    embed.set_thumbnail(url= 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fhedgehog-rainbow.jpg&f=1&nofb=1')
    await ctx.reply(embed = embed)

# sell
@client.command()
async def sell(ctx, item, price): # sell
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.reply("i can't find your numix account, do `>stats` so i make one for ya")
        return
    if item not in acc["inventory"]:
        await ctx.reply("you don't have the item to sell")
        return
    # actually sell the item now
    acc["inventory"].remove(item)
    sellItem(str(ctx.message.author.id), item, price)
    saveChangesToAcc(str(ctx.message.author.id), acc) # save
    await ctx.reply(f"you sold {item} for {price} NumixCoins.")

# jobs list
@client.command()
async def jobs_list(ctx):
    embed = discord.Embed(
        title = f'Jobs - List',
        description = 'what job should you pick? Apply for a job using: `>apply_for_job jobname` (YOU CAN ONLY HAVE 1 JOB AT A TIME)',
        color = discord.Color.purple()
    )
    # embed.add_field(name= f"", value=f'')
    for job in jobs:
        embed.add_field(name= f"{job}", value=f'Amount of numix coins: from {jobs[job][0]} to {jobs[job][1]}')
    embed.set_image(url="https://cdn.discordapp.com/attachments/899208903051591700/899666417262166026/hedgehog_going_to_work.png")
    await ctx.reply(embed=embed)

# job
@client.command()
async def apply_for_job(ctx, jobname, force=None):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.reply("can't find your account, make one using `>stats`")
        return
    if acc["job"] != "" and force != "/force":
        await ctx.reply("you already have a job, to overwrite it, do `>apply_for_job jobname /force`")
        return
    if jobname not in jobs:
        await ctx.reply(f"{jobname} might be a job irl but it isn't in my place.")
        return
    acc["job"] = jobname
    saveChangesToAcc(str(ctx.message.author.id), acc)
    await ctx.reply(f"You have applied for {jobname}, use `>work` to start working and doin business :moneybag:")

# work
@client.command()
async def work(ctx):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.reply("can't find your account, make one using `>stats`")
        return
    if acc["job"] == "":
        await ctx.reply("you got no job, get one by running `>jobs_list` and `>apply_for_job jobname`")
    if acc["job"] not in jobs and acc["job"] != "":
        await ctx.reply(f"Internal error: 'job' key in account is invalid, cannot find {acc['job']} in jobs list (you can do `>fixDb` to fix this)")
        return
    if acc["job"] == "shop":
        await ctx.reply("Working in shop")
        time.sleep(0.1)
        await ctx.reply("You can work in shop with actual users buying your stuff, you want that? (20 seconds to answer) (1=Ye 2=No i dont want to wait 5 years) (Choose a number)")
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        msg = msg.content
        if msg == "1":
            await ctx.reply("Sell an item manually or pick from list? (1=Manually 2=Pick from list) (20 seconds to answer)")
            option = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            option = option.content
            if option == "1":
                await ctx.reply("Run `>sell itemname price`.")
            elif option == "2":
                items_list = [rnd.choice(
                    [s for s in items.keys()]
                ) for i in range(rnd.randint(2, 5))]

                prices = [rnd.randint(1, 30) for i in range(len(items_list))]
                list_str = ""
                for i in range(len(items_list)):
                    list_str += f"{i}. Sell {items_list[i]} for {prices[i]} NCOINS | "
                await ctx.reply(f"List: {list_str}")
                await ctx.reply(f"Chose using the option number you want")
                await ctx.reply("(20 seconds to answer)")
                tosell = await client.wait_for('message', check=lambda message: message.author == ctx.author)
                tosell = int(tosell.content)
                if tosell >= len(items_list):
                    await ctx.reply("bruh, your number is not in the list")
                else:
                    await ctx.reply(f"Alright, you want to sell {items_list[tosell]} for {prices[tosell]} NCOINS")
                    await sell(ctx, items_list[tosell], prices[tosell])
                    await ctx.reply("sold")
        if msg == "2":
            amt = rnd.randint(jobs["shop"][0], jobs["shop"][1])
            acc["coins"] += amt
            saveChangesToAcc(str(ctx.message.author.id), acc)
            await ctx.reply(f"you sold an item for a customer, you just got {amt} numixcoins")
# quit job
@client.command()
async def quit_job(ctx):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.reply("can't find your account, make one using `>stats`")
        return
    acc["job"] = ""
    saveChangesToAcc(str(ctx.message.author.id), acc)
    await ctx.reply("you quit your job")

# batchquest
@client.command()
async def batchquest(ctx, arg=None):
    args = ["--try_to_run", "--latest_download"]
    if arg not in args and arg != None:
        await ctx.reply("WARNING: that argument doesnt exist")
    server = "https://discord.gg/DyQGuanpbT"
    embed = discord.Embed(
        title = f'BatchQuest - Game Made In Batch',
        description = 'didn\'t even know this was possible :flushed:',
        color = 0xeeffee
    )
    embed.add_field(name="Server", value=f"{server}")
    embed.add_field(name="Latest Fetched Download", value=f"https://cdn.discordapp.com/attachments/898610725772218378/899308389245546526/BatchQuest.zip")
    file = discord.File("bg_announcement.png", filename="bq_announcement.png")
    embed.set_image(url="attachment://bq_announcement.png")
    await ctx.reply(file = file, embed = embed)

# safe exit
@commands.is_owner()
@client.command()
async def safe_exit(ctx):
    await ctx.reply("Begin of safe_exit")
    await ctx.reply("Running async_on_exit routine")
    await async_on_exit()
    await ctx.reply("change da world, goodbye")
    await client.close()

# fight
@client.command()
async def fight(ctx, with_: discord.Member):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.reply("can't find your account, make one using `>stats`")
        return
    with_acc = getAcc(str(with_.id))
    if with_acc == "USER_NOT_FOUND":
        await ctx.reply(f"can't find {with_}'s account, make one using `>stats`")
        return
    hp = {
        f"{with_.id}": 100,
        f"{str(ctx.message.author.id)}": 100
    }
    doubt = ""
    if acc["strength"] > with_acc["strength"]:
        doubt = f"<@!{with_.id}>"
    if acc["strength"] < with_acc["strength"]:
        doubt = f"<@!{str(ctx.message.author.id)}>"
    await ctx.reply("STARTING FIGHT!")
    time.sleep(0.1)
    await ctx.reply("You both have 100 HP")
    time.sleep(0.1)
    await ctx.reply(f"Although i doubt {doubt} will win...")
    time.sleep(0.1)
    await ctx.reply("anyways what am i talking about.")
    time.sleep(0.1)
    await ctx.reply("3")
    time.sleep(0.5)
    await ctx.reply("*2*")
    time.sleep(0.5)
    await ctx.reply("***1***")
    time.sleep(0.5)
    await ctx.reply("GO!")

    for i in range(10):
        uid = ""
        opponent_uid = ""
        if i % 2 == 0: 
            uid = str(with_.id)
            opponent_uid = str(ctx.message.author.id)
        else:
            uid = str(ctx.message.author.id)
            opponent_uid = str(with_.id)

        await ctx.reply(f'Chose your option <@!{uid}>: [PUNCH, DEFEND, do nothing and cry in corner (alias: cry)]')
        option = await client.wait_for('message', check=lambda message: [message.author.id == uid, print(uid)])
        option = option.content.lower()

        if option == "punch":
            dmg = rnd.randint(5, 10)
            await ctx.reply(f"<@!{uid}> **punched** his opponent! dealt {dmg} HP!")
            hp[opponent_uid] -= dmg
        elif option == "defend":
            dmg = rnd.randint(5, 10)
            await ctx.reply(f"<@!{uid}> **defended** and dodged a hit, he saved {dmg} HP, he protecc")
        elif option == "cry" or option == "do nothing and cry in corner":
            dmg = rnd.randint(5, 10)
            await ctx.reply(f"<@!{uid}> rn: https://cdn.discordapp.com/attachments/899207967965065286/900051887095701514/video0-10-2.mp4")
        
        else:
            await ctx.reply(f"{option} wasn't in the options")
        if hp[uid] <= 0:
            await ctx.reply(f"<@!{uid}> lost f in chat")
            return
        if hp[opponent_uid] <= 0:
            await ctx.reply(f"<@!{opponent_uid}> lost f in chat")   
            return     

# 100% real hack
@client.command()
async def hack(ctx, who: discord.Member):
    pwd = rnd.choice(["amogus4145#@#", "p@ssw0rd", "*$&*($@URNN$(", "IhaveFriendsIPromise420", f"{who.name}_pwd"])
    email = rnd.choice([f"{who.name}_has_freidns@gmail.com", f"xx{who.name}xx@gmail.com", f"{who.name}_yt@email.com"])
    await ctx.reply(r"Beginning of 100% real hack")
    await ctx.reply(f"Hacking discord account of {who.name}")
    await ctx.reply("10%")
    await ctx.reply("27%")
    await ctx.reply("50%")
    await ctx.reply("-1%")
    await ctx.reply("90%")
    await ctx.reply(f"100% less goo")
    await ctx.reply(f"""Most recent dm: `{
            rnd.choice(["dude the earth is flat i can prove it, also no the doctor did not say i was stupid",
                "fartnite gud",
                "go sub to my yt",
                "join join join join join",
                "can u give free bobux now"
            ])
        }`""")
    await ctx.reply("Installed trojan :troll:")
    await ctx.reply(f"Credentials: \n Email: `{email}`\n Password: {pwd}")
    await ctx.reply(f"Credit card number: {rnd.choice(['346137263040191', '344264969945978', '371063792884107', '340857381975269'])}")
    await ctx.reply("Selling data to government...")
    await ctx.reply("+10,000$ from fbi")
    await ctx.reply(r"the 100% real hack i promise has finished")

@client.command()
async def roulette(ctx):
    await ctx.reply(rnd.choice(["gg you alive leess goo!!!11", "you died, F"]))

# show pc specs
@client.command()
async def pc_specs(ctx):
    acc = getAcc(str(ctx.message.author.id))
    embed = discord.Embed(
        title = f'Pc - Specs',
        description = 'dat pc doe',
        color = 0x00a6ff
    )
    embed.add_field(name="CPU", value=acc["laptop_specs_cpu"])
    embed.add_field(name="GPU", value=acc["laptop_specs_gpu"])
    embed.add_field(name="RAM", value=acc["laptop_specs_ram"])
    embed.add_field(name="DISK", value=acc["laptop_specs_storage_media"])
    embed.add_field(name="OS", value=acc["laptop_os"])
    await ctx.reply(embed = embed)


client.run(open("SECRET_FOLDER/token.txt", "r").read())