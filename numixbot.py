from inspect import indentsize
from itertools import permutations
from typing import Text
from attr import field
import discord
from discord import channel
from discord import integrations
from discord.client import Client
from discord.embeds import Embed
from discord.ext import commands
import random
rnd = random
import aiohttp
from discord.flags import Intents
import os
import asyncio as asio
import json
import time
from discord.ext.commands import cooldown, BucketType

intents = discord.Intents.default()
intents.members = True
client_ = discord.Client(intents=intents)

client = commands.Bot(command_prefix=">", help_command=None)
numixAccFile = "numixAccs.json"
utilities = ["PHONE_UTILITY", "CAN_BE_EATEN", "CAN_FISH", "CAN_SHOOT_PEOPLE", "CAN_SHOOT_DEMONS"]
items_not_in_shop = ["demon_destroyer"]
accStructure = {
    "coins": 0,
    "inventory": [],
    "strength": 0,
    "stamina": 0
}
foods = {
    #"FOODNAME": STAMINA_AMT
    "apple": 1,
    "fish":  2,
    "le_fishe_au_chocolat": 5
}
items = {
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
    }
}

@client.event
async def on_ready():
    print("Logged in.")
    with open(numixAccFile, "r+") as f:
        if f.read() == "":
            f.write(json.dumps({}))
        

# async def do_request(url):
#     print(f"do_request called with url={url}")
#     async with aiohttp.ClientSession().get(url=url) as data:
#         return data

def max_idx(l):
    idx, biggest = (0, 0)
    cIdx = 0
    for elem in l:
        if elem > biggest:
            biggest = elem
            idx = cIdx
    return idx
def getAcc(id):
    file = json.load(open(numixAccFile, "r"))
    if id in file:
        return file[id]
    return "USER_NOT_FOUND"
def createAcc(username):
    struct = accStructure
    file = json.load(open(numixAccFile, "r"))
    file[username] = struct
    with open(numixAccFile, "w") as f:
        f.write(json.dumps(file))
def readAccsFile():
    return json.load(open(numixAccFile, "r"))
def getItem(name):
    if item not in name:
        return "ITEM_NOT_FOUND"
    return items[name]
def saveChangesToAcc(id, changes):
    file = json.load(open(numixAccFile, "r"))
    file[id] = changes
    with open(numixAccFile, "w") as f:
        f.write(json.dumps(file))
# Commands

# Help command

@client.command(name= 'help')
async def help(ctx):
    embed = discord.Embed(
        title = 'Help',
        description = 'Help page',
        color = discord.Color.green()
    )
    embed.add_field(name= 'General', value='`hedgehog`')
    embed.add_field(name= 'Fun', value= '`meme` ' '`poll` ' '`ping` `say` `spoopy` `stats` `transfer_coins` `shop` `buy` `jackpot` `use_item`', inline=False)
    embed.add_field(name= 'Moderation', value= '`ban` ' '`kick` ' '`lockdown` ' '`unlock`', inline=False)
    embed.set_image(url= 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fcute-hedgehog-bath.jpg&f=1&nofb=1')
    embed.set_thumbnail(url= 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fhedgehog-rainbow.jpg&f=1&nofb=1')
    await ctx.send(embed=embed)



# Lockdown and unlock commands

# Lockdown command

@client.command()
@commands.has_permissions(manage_channels = True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + " is in lockdown...")

# unlock command

@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " has been successfully unlocked!")



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
          await member.kick(reason=reason)
      except:
          await ctx.send("The member has their DMS closed.")
          await member.kick(reason=reason)
    else:
        await ctx.send('You do not have the permissions required.')

# Mute command

@client.command()
async def mute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_message=False, speak=False)
        await guild.create_role(name="muted", permutations=perms)
        await member.add_roles(role)
        await ctx.send(f"{member} was muted.")
    else:
        await member.add_roles(role)
        await ctx.send(f"{member} was muted.")

# Hedgehogs commands

@client.command()
async def hedgehog(ctx):
    async with aiohttp.ClientSession().get(url="https://www.reddit.com/r/Hedgehogs/.json") as data:
        if data.status == 200:
            hedgehogs = await data.json(content_type=None)
            embed = discord.Embed(
                color = discord.Color.purple()
            )
            embed.set_image(url=hedgehogs["data"]["children"][random.randint(0, 25)]["data"]["url"]),
            embed.set_footer(text=f"Powered by r/Hedgehogs | Hedgehog requested by {ctx.author}"),
            await ctx.send(embed=embed)
        else:
            await ctx.send("reddit sent not good status: " + str(data.status))



# Fun

# Memes commands

@client.command()
async def meme(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/memes/.json") as r:
           memes = await r.json(content_type=None)
           embed = discord.Embed(
               color = discord.Color.purple()
           )
           embed.set_image(url=memes["data"]["children"][random.randint(0, 25)]["data"]["url"]),
           embed.set_footer(text=f"Powered by r/memes | Meme requested by {ctx.author}"),
           await ctx.send(embed=embed)



# Ping and pong

@client.command()
async def ping(ctx):
    await ctx.send("pong, -0 ms")



# Poll command

@client.command()
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL 📣", description=f"{message}", text=f"Poll requested by {ctx.author}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('⬆️')
    await msg.add_reaction('⬇️')



# Errors

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You don't have permissions to do that.")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please enter the required argument.")
        await ctx.message.delete()
    elif isinstance(error,commands.MemberNotFound):
        await ctx.send("This member do not exist.")
        await ctx.message.delete()
    elif isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"take a chill pill",description=f"Try again in {error.retry_after:.2f}s. This command is on cooldown.", color=discord.Color.red())
            await ctx.send(embed=em)
    else:
        raise error

# Say command
@client.command()
async def say(ctx, *, msg):
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(msg)

# spoopy

@client.command()
async def spoopy(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/885888076260454461/897169777045430303/unknown.png")

# Numix Acc stats

@client.command()
async def stats(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.message.author
    account = getAcc(str(user.id))
    if account == "USER_NOT_FOUND":
        await ctx.send("I can't find your numix account, ima create one real quick...")
        createAcc(str(user.id))
    embed = discord.Embed(
        title = f'Account Stats - {user.name}',
        description = 'Stat page',
        color = discord.Color.green()
    )
    formattedInv = ""
    inv = account["inventory"]
    for item in inv:
        formattedInv += f"{item}\n"
    embed.add_field(name= 'Coins', value=f'`{account["coins"]}`')
    embed.add_field(name= 'Inventory', value=f'`{formattedInv}`')
    embed.add_field(name= 'Strength', value=f'`{account["strength"]}`')
    embed.add_field(name= 'Stamina', value=f'`{account["stamina"]}`')
    embed.set_thumbnail(url= 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fhedgehog-rainbow.jpg&f=1&nofb=1')
    await ctx.send(embed = embed)

# Fix database
@client.command()
async def fixDb(ctx):
    msg = await ctx.send("Beggining to fix bad stuff inside db...")
    db = json.load(open(numixAccFile, "r"))
    fixedTotal = 0
    for key in db:
        acc = db[key]
        for s in accStructure:
            if s not in acc:
                acc[s] = accStructure[s]
                fixedTotal += 1
                await msg.edit(content=f"Fixed {fixedTotal} bad stuff, the {s} key was missing. Continuing...")
                print(f"Fixed {fixedTotal} bad stuff, the {s} key was missing. Continuing...")
        acc2 = acc.copy()
        for aitm in acc:
            if aitm not in accStructure:
                del acc2[aitm]
                fixedTotal += 1
                await msg.edit(content=f"Fixed {fixedTotal} bad stuff, the {aitm} key was an invalid key. Continuing...")
                print(f"Fixed {fixedTotal} bad stuff, the {aitm} key was an invalid key. Continuing...")
        db[key] = acc2.copy()
        del acc2
    with open(numixAccFile, "w") as f:
        f.write(json.dumps(db))
    await ctx.send(f"End. Fixed {fixedTotal} bad stuff.")

# Shop
@client.command()
async def shop(ctx):
    embed = discord.Embed(
        title = f'Shop',
        description = 'let\'s buy stuff',
        color = discord.Color.red()
    )
    for item in items:
       if item not in items_not_in_shop:
           embed.add_field(name= f"*Name*: {item}", value=f'`Cost: {items[item]["price"]} NumixCoins`')
    embed.set_thumbnail(url= 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fhedgehog-rainbow.jpg&f=1&nofb=1')
    await ctx.send(embed = embed)

# Buy
@client.command()
async def buy(ctx, itemname):
    if itemname not in items:
        await ctx.send("that item doesnt exist bruh")
    account = getAcc(str(ctx.message.author.id))
    if account == "USER_NOT_FOUND":
        await ctx.send("use `>stats` to create a numix account because you don't have one")
    else:
        if account["coins"] < items[itemname]["price"]:
            await ctx.send("you don't have enough money to buy this item.")
        else:
            account["coins"] -= items[itemname]["price"]
            account["inventory"].append(itemname)
            await ctx.send(f"You bought `{itemname}`, do `>stats` to see the item in your inventory")
    saveChangesToAcc(str(ctx.message.author.id), account)

# Transfer Coins
@client.command()
async def transfer_coins(ctx, to: discord.Member = None, amt: int = None):
    if to == None:
        await ctx.send("I need to transfer some coins to someone, can't transfer to no one")
        return
    if amt == None:
        await ctx.send("how much do you want to send? i cant read your mind")
        return
    user  = getAcc(str(ctx.message.author.id))
    to_   = getAcc(str(to.id))
    if user == "USER_NOT_FOUND":
        await ctx.send("can't find your account, do `>stats` so i can create one for u")
        return
    if to_  == "USER_NOT_FOUND":
        await ctx.send(f"can't find the account of {to.name}, make them do `>stats` so i will make them an account")
        return
    if user["coins"] < amt:
        await ctx.send("you don't have enough coins")
        return
    user["coins"] -= amt
    to_ ["coins"] += amt
    saveChangesToAcc(str(ctx.message.author.id), user)
    saveChangesToAcc(str(to.id)                , to_ )
    await ctx.send(f"Transfered {amt} coin(s) to {to.name}")

# Jackpot
@commands.cooldown(1, 30, commands.BucketType.user)
@client.command()
async def jackpot(ctx):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.send("can't find your account, do `>stats`")
        return 
    await ctx.send("🎲 Rolling...")
    rolls = ["😦", "😕", "🙂", "😳", "💰"]
    rolls_cost = {
        "😦": 2, 
        "😕": 6, 
        "🙂": 20, 
        "😳": 40, 
        "💰": 60
    }
    rolled = [
        rnd.choice(rolls), 
        rnd.choice(rolls), 
        rnd.choice(rolls)
    ]
    await ctx.send(f"{rolled[0]} `?` `?`")
    time.sleep(0.1)
    await ctx.send(f"{rolled[0]} {rolled[1]} `?`")
    time.sleep(0.1)
    await ctx.send(f"{rolled[0]} {rolled[1]} {rolled[2]}")
    
    
    amt = 0
    
    luck = rolls_cost[rolled[0]] + rolls_cost[rolled[1]] + rolls_cost[rolled[2]]
    chose = False
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
    
    acc["coins"] += amt
    saveChangesToAcc(str(ctx.message.author.id), acc)
    await ctx.send(f"You won {amt} coins")

# Use item
@client.command()
async def use_item(ctx, itemname, phone_arg: discord.Member = None):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.send("can't find your account, do `>stats`")
        return 
    if itemname not in acc["inventory"]:
        await ctx.send("you don't have this item")
        return
    utility = items[itemname]["utility"]
    for util in utility:
        if util not in utilities:
            await ctx.send(f"Internal Error: {util} is not a valid utility")
            return
    await ctx.send(f"Using {itemname}.")
    for util in utility:
        if util == "PHONE_UTILITY":
            if phone_arg == None:
                await ctx.send("Provided the required argument: `>use_item itemname PERSON_TO_TEXT`")
                return
            dm = await phone_arg.create_dm()
            await ctx.send("What message do you want to send? (You have 20 seconds)")
            msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
            await dm.send(f"**Sent from {ctx.message.author.name}'s phone: ** {msg.content}")
        if util == "CAN_BE_EATEN":
            if itemname not in foods:
                await ctx.send(f"Internal error: {itemname} has utility 'CAN_BE_EATEN' but is not marked in the 'foods' list.")
                return
            acc["stamina"] += foods[itemname]
            acc["inventory"].remove(itemname)
            saveChangesToAcc(str(ctx.message.author.id), acc)
            await ctx.send(f"you ate {itemname} and got {foods[itemname]} stamina")
        if util == "CAN_FISH":
            fished = rnd.randint(0, 5)
            if fished == 5:
                await ctx.send("Got a fish!")
                acc["inventory"].append("fish")
                saveChangesToAcc(str(ctx.message.author.id), acc)
            else:
                await ctx.send("no fish ;-;")
        if util == "CAN_SHOOT_PEOPLE":
            if phone_arg == None:
                await ctx.send("Use this command as `>use_item shotgun PING_THE_PERSON_YOU_WANT_TO_SHOOT`") 
            if phone_arg != None:
                slost = rnd.randint(1, 8)
                l = getAcc(str(phone_arg.id))
                if l == "USER_NOT_FOUND":
                    await ctx.send("can't find the other user's numix account, make them do `>stats` so i will make them one")
                    return
                if l["strength"] < slost:
                    await ctx.send("they got too low strength, they wont get negative strength")
                    return
                l["strength"] -= slost
                saveChangesToAcc(str(phone_arg.id), l)
                await ctx.send(f"Shot {phone_arg.name}, they lost {slost} strength")
        if util == "CAN_SHOOT_DEMONS":
            acc["coins"] += 9
            saveChangesToAcc(str(ctx.message.author.id), acc)
            await ctx.send("KILLED A DEMON +9 NUMIX COIN FOR HELPING SUSCIETY.")
# Do sports
@client.command()
async def do_sports(ctx, lvl: str = None):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.send("can't find your account, do `>stats`")
        return
    if lvl == None:
        await ctx.send("What level of sports do you want to do (easy, medium, hard)? (20 seconds to answer)")
        msg = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content not in ["easy", "medium", "hard"]:
            await ctx.send("bruh, that is not a sport level")
            return
        level = msg.content
    else:
        if lvl not in ["easy", "medium", "hard"]:
            await ctx.send("bruh, that is not a sport level")
            return
        level = lvl
    if level == "easy":
        if acc["stamina"] < 3:
            await ctx.send("not enough stamina, need 3 stamina")
            return
        stoadd = rnd.randint(1, 3)
        acc["strength"] += stoadd
        acc["stamina"] -= 3
        saveChangesToAcc(str(ctx.message.author.id), acc)
        await ctx.send(f"you did an easy session of sports, +{stoadd} strength, -3 stamina")
        return
    if level == "medium":
        if acc["stamina"] < 5:
            await ctx.send("not enough stamina, need 5 stamina")
            return
        stoadd = rnd.randint(5, 8)
        acc["strength"] += stoadd
        acc["stamina"] -= 5
        saveChangesToAcc(str(ctx.message.author.id), acc)
        await ctx.send(f"you did a medium session of sports, +{stoadd} strength, -5 stamina")
        return
    if level == "hard":
        if acc["stamina"] < 8:
            await ctx.send("not enough stamina, need 8 stamina")
            return
        stoadd = rnd.randint(9, 14)
        acc["strength"] += stoadd
        acc["stamina"] -= 8
        saveChangesToAcc(str(ctx.message.author.id), acc)
        await ctx.send(f"you did a hard session of sports, +{stoadd} strength, -8 stamina")
        return

# leaderboard
@client.command()
async def leaderboard(ctx):
    embed = discord.Embed(
        title = f'Leaderboard',
        description = 'best users',
        color = discord.Color.red()
    )
    accounts = []
    depth = 4
    costs = {}
    accs = readAccsFile()
    cIdx = 0

    for acc in accs:
        if cIdx >= depth:
            break
        cost = accs[acc]["strength"] + accs[acc]["stamina"] + accs[acc]["coins"]
        costs[int(cost)] = (acc, accs[acc].copy())
        cIdx += 1

    for acc in costs.items():
        accounts.append(acc)

    bestUser = False
    for i in range(depth):
        add = ""
        if not bestUser:
            add = "🏆"
            bestUser = True
        acc__ = [s for s in accounts[i]]
        print(acc__)
        embed.add_field(name= f"{add}{acc__[1][0]}", value=f'(**<@!{acc__[1][0]}>**) Coins: {acc__[1][1]["coins"]} | Stamina: {acc__[1][1]["stamina"]} | Strength: {acc__[1][1]["strength"]}')
    
    embed.set_thumbnail(url= 'https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fthefunnybeaver.com%2Fwp-content%2Fuploads%2F2018%2F06%2Fhedgehog-rainbow.jpg&f=1&nofb=1')
    await ctx.send(embed = embed)

@client.command()
async def sell(ctx, item):
    acc = getAcc(str(ctx.message.author.id))
    if acc == "USER_NOT_FOUND":
        await ctx.send("i can't find your numix account, do `>stats` so i make one for ya")
    
client.run("ODk3MTQ4NzIwNjQ5NDY5OTg1.YWRc2w.6V4fYgO7sAWlm3xkOAgbTib_JtY")