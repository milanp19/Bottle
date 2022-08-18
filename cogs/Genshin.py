from http.client import HTTPException
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
        
        
        with open(f"data/characters/{char}/en.json", 'r') as f1:

            data = json.load(f1)
            try:
                embed = discord.Embed(title = "Character", timestamp = ctx.message.created_at)
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
            embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
            await ctx.send(embed=embed,file=file)

    @commands.command()
    async def weapon(self, ctx):
    
        
        weapons = os.listdir("data/weapons/")
        weapon = choice(weapons)
        
        
        with open(f"data/weapons/{weapon}/en.json", 'r') as f1:

            data = json.load(f1)
            try:
                embed = discord.Embed(title = "Weapon", timestamp = ctx.message.created_at)
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
        




async def setup(client):
    await client.add_cog(Genshin(client))