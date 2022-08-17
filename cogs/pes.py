from discord.ext import commands
import discord
import random
import asyncio
#import math
import requests
from bs4 import BeautifulSoup
import aiohttp

class Pes(commands.Cog):
    def __init__(self, client):
        self.client = client


    async def button_stat(self,ctx,stats,t):
        embed = discord.Embed(title = f"Wow {ctx.author.name}, you packed:", description="", color=0xFFFFF, timestamp = ctx.message.created_at)
        embed.add_field(name = "Name:", value = stats["name"], inline = False)
        embed.add_field(name = "Rating:", value = stats["rating"], inline = False)
        embed.add_field(name = "Position:", value = stats["position"], inline = False)
        #embed.set_thumbnail(url = urls)
        embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
        embed.set_image(url = stats["image_url"])
        embed.set_thumbnail(url = t)
  
        await ctx.send(embed=embed)  
        await ctx.send("**Good Pull or scripted?** <:help:843403016379826186>")

    @commands.command()
    @commands.cooldown(1,17,commands.BucketType.user)
    async def legend(self,ctx):
        #await ctx.send("command has been disabled due to technical issues,pls try out other commands named regular,rps or tictactoe while this is fixed")
        url = "https://imgur.com/a/vUBZap7"
        t = "https://images-ext-1.discordapp.net/external/d3bYXLQyw480r6MAFFNAAKue2-XlnVWqaNl067aU1fo/%3Fwidth%3D406%26height%3D406/https/media.discordapp.net/attachments/788705918589468674/836131117861437450/legends_gif.gif"

        a = await ctx.send(url)
        await asyncio.sleep(6.4)
        page_number = random.randint(0, 2)
        async with aiohttp.ClientSession() as leg:
            async with leg.get(f"https://www.pesmaster.com/pes-2021-mobile/search/api.php?game=2021mobile&type=legend&page={page_number}") as r:
                data =  await r.json()
                rand_player = random.randint(0, len(data["data"]) - 1)
                name = data["data"][rand_player]['name']
                rating = str(data["data"][rand_player]['ovr']) + " - " + str(data["data"][rand_player]['pot'])
                position = data["data"][rand_player]['pos']
                image = data["data"][rand_player]['image'] 
                player_url = data["data"][rand_player]['url']   

                stats = {
                "name": name,
                "rating": rating,
                "position": position, 
                "image_url": f"https://www.pesmaster.com{image}",
                "player_url": player_url
            }    
        await a.delete()
        
        await self.button_stat(ctx,stats,t)


    
    @commands.command()
    @commands.cooldown(1,17,commands.BucketType.user)
    async def iconic(self,ctx):
        #await ctx.send("command has been disabled due to technical issues,pls try out other commands named regular,rps or tictactoe while this is fixed")
        url = "https://imgur.com/a/QfG4DbN"
        t = "https://images-ext-2.discordapp.net/external/aPquMg5wJwkBtlImBGrfI_M9pJ85R2i_2nPYf2danSM/https/media.discordapp.net/attachments/723015304439136316/836309933317685319/iconic1.gif"
        a = await ctx.send(url)
        await asyncio.sleep(6.2)
        page_number = random.randint(0, 4)
        async with aiohttp.ClientSession() as leg:
            async with leg.get(f"https://www.pesmaster.com/pes-2021-mobile/search/api.php?game=2021mobile&type=IconicMoment&page={page_number}") as r:
                data =  await r.json()
                rand_player = random.randint(0, len(data["data"]) - 1)
                name = data["data"][rand_player]['name']
                rating = str(data["data"][rand_player]['ovr']) + " - " + str(data["data"][rand_player]['pot'])
                position = data["data"][rand_player]['pos']
                image = data["data"][rand_player]['image'] 
                player_url = data["data"][rand_player]['url']   

                stats = {
                "name": name,
                "rating": rating,
                "position": position, 
                "image_url": f"https://www.pesmaster.com{image}",
                "player_url": player_url
                }   
        await a.delete()

        await self.button_stat(ctx,stats,t)

    @commands.command()
    @commands.cooldown(1,17,commands.BucketType.user)
    async def featured(self,ctx):
        #await ctx.send("command has been disabled due to technical issues,pls try out other commands named regular,rps or tictactoe while this is fixed")
        url = "https://imgur.com/a/AC0hCTj"
        t = "https://media.discordapp.net/attachments/865565483435294732/892104790199390249/ezgif.com-gif-maker_1.gif"

        a = await ctx.send(url)
        await asyncio.sleep(5.3)
        page_number = random.randint(0, 57)
        async with aiohttp.ClientSession() as leg:
            async with leg.get(f"https://www.pesmaster.com/pes-2021/search/api.php?game=2021&type=featured&page={page_number}") as r:
                data =  await r.json()
                rand_player = random.randint(0, len(data["data"]) - 1)
                name = data["data"][rand_player]['name']
                rating = str(data["data"][rand_player]['ovr']) + " - " + str(data["data"][rand_player]['pot'])
                position = data["data"][rand_player]['pos']
                image = data["data"][rand_player]['image'] 
                player_url = data["data"][rand_player]['url']   

                stats = {
                "name": name,
                "rating": rating,
                "position": position, 
                "image_url": image,
                "player_url": player_url
                }
        await a.delete()
        
        await self.button_stat(ctx,stats,t)



      

    @commands.command()
    @commands.cooldown(1,17,commands.BucketType.user)
    async def spin(self,ctx):
        #await ctx.send("command has been disabled due to technical issues,pls try out other commands named regular,rps or tictactoe while this is fixed")
        k = random.choices(["iconic","legend","featured"], weights = [5, 10, 15])
        if k[0] == "iconic":
            await self.iconic(self, ctx)
        elif k[0] == "legend":
            await self.legend(self,ctx)
        elif k[0] == "featured":
            await self.featured(self,ctx)

        
async def setup(client):
    await client.add_cog(Pes(client))