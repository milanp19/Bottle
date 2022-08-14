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
    
        chars = os.listdir('../assets/data/characters/')
        char = choice(chars)
        

        with open(f"../data/characters/{char}/en.json", 'r') as f1, Image.open(f"../images/characters/{char}/portrait") as l:

            data = json.load(f1)

            embed = discord.Embed(title = data['name'])

            embed.add_field(name = 'Nation', value=data['nation'], inline = False)
            embed.add_field(name = 'Vision', value=data['vision'], inline = False)
            embed.add_field(name = 'Weapon', value=data['weapon'], inline = False)
        
        

            #l.save('mm.jpg')
            l  = l.convert("RGBA")

            im = l.resize((round(l.size[0]*2), round(l.size[1]*2)))
            
            im.save("mm.png")
            file=discord.File("mm.png", filename="mm.png")


            embed.set_image(url = "attachment://mm.png")



        
        #embed.set_thumbnail(url = "")
        embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
        await ctx.send(embed=embed,file = file)




async def setup(client):
    await client.add_cog(Genshin(client))