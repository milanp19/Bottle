import discord
from discord.ext import commands
import os
from random import choice
import json
from PIL import Image



class Genshin(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def roll(self, ctx):
    
        
        chars = os.listdir("data/characters/")
        char = choice(chars)
        
        try:
            with open(f"data/characters/{char}/en.json", 'r') as f1, Image.open(f"images/characters/{char}/portrait") as l:

                data = json.load(f1)

                embed = discord.Embed(title = "Character")
                embed.add_field(name = 'Name', value=data['name'], inline = True)
                embed.add_field(name = 'Vision', value=data['vision'], inline = True)
                embed.add_field(name = 'Nation', value=data['nation'], inline = True)
                embed.add_field(name = 'Weapon', value=data['weapon'], inline = True)
                embed.add_field(name = 'Rarity', value=data['rarity'] * '⭐', inline = True)
                embed.add_field(name = 'Birthday', value=data['birthday'][5:] or 'N/A', inline = True)
                embed.add_field(name = 'Description', value=data['description'], inline = True)
                
            
                l  = l.convert("RGBA")
                l.save("mm.png")
                file=discord.File("mm.png", filename="mm.png")
                embed.set_image(url = "attachment://mm.png")
                embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
                await ctx.send(embed=embed,file = file)
        except FileNotFoundError:
            with open(f"data/characters/{char}/en.json", 'r') as f1:

                data = json.load(f1)

                embed = discord.Embed(title = "Character")
                embed.add_field(name = 'Name', value=data['name'], inline = True)
                embed.add_field(name = 'Vision', value=data['vision'], inline = True)
                embed.add_field(name = 'Nation', value=data['nation'], inline = True)
                embed.add_field(name = 'Weapon', value=data['weapon'], inline = True)
                embed.add_field(name = 'Rarity', value=data['rarity'] * '⭐', inline = True)
                embed.add_field(name = 'Birthday', value=data['birthday'][5:] or 'N/A', inline = True)
                embed.add_field(name = 'Description', value=data['description'], inline = True)
        

                embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
                await ctx.send(embed=embed)




async def setup(client):
    await client.add_cog(Genshin(client))