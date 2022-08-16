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

                embed = discord.Embed(title = data['name'])
                embed.add_field(name = 'Nation', value=data['nation'], inline = False)
                embed.add_field(name = 'Vision', value=data['vision'], inline = False)
                embed.add_field(name = 'Weapon', value=data['weapon'], inline = False)
            
                l  = l.convert("RGBA")
                l.save("mm.png")
                file=discord.File("mm.png", filename="mm.png")
                embed.set_image(url = "attachment://mm.png")
                embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
                await ctx.send(embed=embed,file = file)
        except FileNotFoundError:
            with open(f"data/characters/{char}/en.json", 'r') as f1:

                data = json.load(f1)

                embed = discord.Embed(title = data['name'])
                embed.add_field(name = 'Nation', value=data['nation'], inline = False)
                embed.add_field(name = 'Vision', value=data['vision'], inline = False)
                embed.add_field(name = 'Weapon', value=data['weapon'], inline = False)
        

                embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
                await ctx.send(embed=embed)




async def setup(client):
    await client.add_cog(Genshin(client))