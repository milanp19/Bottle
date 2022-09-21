from http.client import HTTPException
import discord
from discord.ext import commands
import os
from random import choice,choices
import json
from PIL import Image


class User:
    def __init__(self, id, characters = None, pity = 0, ):
        self.id = id
        if characters == None:
            self.characters = []
        else:
            self.characters = characters
        self.pity = pity

        with open("user_data.json", "r") as file:
            handler = json.load(file)

        handler[self.id] = {

            "characters": self.characters,
            "pity": self.pity

        } 
            
        with open("user_data.json", "w") as file:
            json.dump(handler, file)


    @staticmethod
    def exit(id_1):
        with open("user_data.json", "r") as file:
            handler = json.load(file)
        
        del handler[str(id_1)]

        with open("user_data.json", "w") as file:
            json.dump(handler, file)

            
# # mi = User("123")
# # m2 = User("234")
# chance1 = (i for i in range(1,31))
# chance2 = (i for i in range(31,51))
# chance3 = (i for i in range(51,61))
# chance4 = (i for i in range(61,71))
# chance5 = (i for i in range(71,81))
# chance6 = (i for i in range(81,91))

# pulls_needed = choices([chance1, chance2, chance3, chance4, chance5, chance6], weights = [5,10,15,20,40,15])
# chances = 30#choice(list(pulls_needed[0]))

# pity_counter = 0

# def counter():
#     global pity_counter
#     if pity_counter < 91:
#         pity_counter += 10
#         if pity_counter > chances or pity_counter == chances:
#             print(f"you got 5 star on {chances} pity")
#             #pity_counter = pity_counter - chances
#         print(pity_counter)
#     else: 
#         pity_counter = 0
#         print(pity_counter)


# k = True
# while k:
#     chars = os.listdir("data/characters/")
#     chars5 = os.listdir("data/characters5/")
#     char = choice(chars)
#     char5 = choice(chars5)


#     counter()
#     with open(f"data/characters/{char}/en.json", 'r') as f1, open(f"data/characters5/{char5}/en.json", 'r') as f2:

#         data = json.load(f1)
#         data5 = json.load(f2)
#         if pity_counter == chances:
#             print(data5['name'])
#             k = False

#         elif pity_counter < chances and data['rarity'] == 4:
#             print(data['name'])

# pity_counter = pity_counter - chances
# print(pity_counter)

class Genshin(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def roll(self, ctx):
    
        
        chars = os.listdir("data/characters/")
        char = choice(chars)
        
        
        with open(f"data/characters/{char}/en.json", 'r') as f1:

            data = json.load(f1)
            try:
                embed = discord.Embed(title = "Character")
                embed.add_field(name = 'Name', value=data['name'], inline = True)
                embed.add_field(name = 'Vision', value=data['vision'], inline = True)
                embed.add_field(name = 'Nation', value=data['nation'], inline = True)
                embed.add_field(name = 'Weapon', value=data['weapon'], inline = True)
                embed.add_field(name = 'Rarity', value=data['rarity'] * '⭐', inline = True)
                try:
                    if data['birthday']:
                        embed.add_field(name = 'Birthday', value=data['birthday'][5:], inline = True)
                except KeyError:
                    print("no birthday data")
                    embed.add_field(name = 'Birthday', value='N/A', inline = True)
                embed.add_field(name = 'Description', value=data['description'], inline = True)
                
            
                # l  = l.convert("RGBA")
                # l.save("mm.png")
                try:
                    file=discord.File(f"images/characters/{char}/portrait.png",filename="mm.png")
                    embed.set_image(url = "attachment://mm.png")
                except FileNotFoundError:
                    file = None
                    print(data['name'])
                    print("file not found error")
            except HTTPException:
                print(data['name'])
            embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author} || pity =")
            await ctx.send(embed=embed,file=file)

    @commands.command()
    async def weapon(self, ctx):
    
        
        weapons = os.listdir("data/weapons/")
        weapon = choice(weapons)
        
        
        with open(f"data/weapons/{weapon}/en.json", 'r') as f1:

            data = json.load(f1)
            try:
                embed = discord.Embed(title = "Weapon")
                embed.add_field(name = 'Name', value=data['name'], inline = True)
                embed.add_field(name = 'Type', value=data['type'], inline = True)
                embed.add_field(name = 'Base Attack', value=data['baseAttack'], inline = True)
                embed.add_field(name = 'Sub Stat', value=data['subStat'], inline = True)
                embed.add_field(name = 'Rarity', value=data['rarity'] * '⭐', inline = True)
                embed.add_field(name = 'Location', value=data['location'], inline = True)
                try:
                    embed.add_field(name = f"Passive Name: {data['passiveName']}", value=data['passiveDesc'], inline = False)
                except KeyError:
                    print("weapon passive not available")

                try:
                    file=discord.File(f"images/weapons/{weapon}/icon.png",filename="yes.png")
                    embed.set_thumbnail(url = "attachment://yes.png")
                except FileNotFoundError:
                    file = None
                    print(data['name'])
                    print("no weapon icon")
            except HTTPException:
                print(data['name'])
            embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
            await ctx.send(embed=embed,file=file)
        

    @commands.command()
    async def login(self, ctx):
        #import json
        with open("user_data.json", "r") as file:
            handler = json.load(file)
            #print(handler.keys())
        if str(ctx.author.id) not in handler.keys():
            User(ctx.author.id)
            await ctx.send("Logged in successfully")
        else: await ctx.send("Your're already logged in")


    @commands.command()
    async def deauth(self, ctx):
        User.exit(ctx.author.id)
        await ctx.send("Logged out successfully")


async def setup(client):
    await client.add_cog(Genshin(client))