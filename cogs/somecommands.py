from discord.ext import commands # Again, we need this imported
import discord
import time
import random
import asyncio
from pyfiglet import Figlet
import traceback
import os
from typing import Optional
from discord import utils
import qrcode
import math



class SomeCommands(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, client: commands.Bot):
        self.client = client
        self.last_msg = None
        self.prem_msg = None
        


    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        await message.edit(content=f"Pong! {round(self.client.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")          
    

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
      self.last_msg = message
      if self.last_msg.guild.id == 723004314338984059:
        async for entry in message.guild.audit_logs(limit=1,action=discord.AuditLogAction.message_delete):
          deletedby = entry.user or 'bot'
      
          self.prem_msg = f"{deletedby} deleted message by {message.author}\ncontent: {message.content}"    
          log_channel = self.client.get_channel(902503255970562078)
          embed = discord.Embed(title=f"Message from {message.author}", description=message.content, timestamp = message.created_at)
          embed.set_footer(icon_url=message.author.avatar.url, text = f"deleted by {deletedby}")
          await log_channel.send(embed = embed)
          #self.last_msg = message
        

        # if self.last_msg.guild.id == 723004314338984059:
        #   log_channel = self.client.get_channel(902503255970562078)
          
        #   if message.author.bot is True:
        #     return
        #   else:
        #     author = self.last_msg.author 
        #     content = self.last_msg.content 
        #     attachments = self.last_msg.attachments
        #     att = ""
        #   for i in range(len(attachments)):
        #     att += f"{i+1}. {attachments[i].url}\n"
          
        #   embed = discord.Embed(title=f"Message from {author}", description=content)
        #   if attachments:
        #     embed.add_field(name = "attachments", value = att)
        #   await log_channel.send(embed=embed)


    @commands.command(name="snipe")
    async def snipe(self, ctx: commands.Context):
        """A command to snipe delete messages."""
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_msg.author 
        content = self.last_msg.content 
        attachments = self.last_msg.attachments
        att = ""

        for i in range(len(attachments)):
          att += f"{i+1}. {attachments[i].url}\n"
        

        if ctx.guild == self.last_msg.guild and ctx.channel == self.last_msg.channel:
          embed = discord.Embed(title=f"Message from {author}", description=content)
          if attachments:
            embed.add_field(name = "attachments", value = att)
          await ctx.send(embed=embed)
        else:
          await ctx.send("There is no message to snipe!")
          return

    @commands.has_permissions(administrator=True)
    @commands.command(name="s")
    async def s(self, ctx: commands.Context):
        """A command to snipe delete messages and know who deleted the msg."""
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            await ctx.send("There is no message to snipe!")
            return
        attachments = self.last_msg.attachments
        att = ""

        for i in range(len(attachments)):
          att += f"{i+1}. {attachments[i].url}\n"

        embed = discord.Embed(title="Premium Snipe", description=self.prem_msg)
        if att:
          embed.add_field(name="attachments", value=att)
        await ctx.send(embed=embed)


    @commands.command()
    async def say(self,ctx, user: Optional[discord.Member], *msg):
      msg = msg or "say"
      user = user or ctx.author
      l=""
      for i in msg:
            l+=f"{i} "
      
      webhooks = await ctx.channel.webhooks()      
      webhook = utils.get(webhooks, name = "imposter")
      if webhook is None:
        webhook = await ctx.channel.create_webhook(name = "imposter")
      await webhook.send(l, username = user.name, avatar_url = user.avatar_url)
      await ctx.message.delete()
    

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
      self.bef = before 
      self.aft = after 
      if not self.aft: 
        return
      
      else:
        if self.aft.embeds:
          return
        author = self.bef.author
        content1 = self.bef.content 
        content2 = self.aft.content
      

      if self.bef.guild.id == 829772719427551253:
          log_channel = self.client.get_channel(902503255970562078)
          embed = discord.Embed(title="", description=f"**before**:\n {content1}")
          embed.add_field(name = "after:", value = content2)
          embed.set_author(name = author, icon_url = author.avatar_url)
          await log_channel.send(embed=embed)

      
    @commands.command()
    async def esnipe(self, ctx: commands.Context):
        #A command to snipe delete messages.
        if not self.bef or not self.aft: 
            await ctx.send("There is no message to snipe!")
            return

        author = self.bef.author
        content1 = self.bef.content 
        bef_attachments = self.bef.attachments
        att = ""

        for i in range(len(bef_attachments)):
          att += f"{i+1}. {bef_attachments[i].url}\n"

        content2 = self.aft.content 


        if ctx.guild == self.bef.guild and ctx.channel == self.bef.channel:
          embed = discord.Embed(title="", description=f"**before**:\n {content1}")
          if bef_attachments:
            embed.add_field(name = "attachments", value = att, inline = False)
          embed.add_field(name = "after:", value = content2)
          embed.set_author(name = author, icon_url = author.avatar.url)
          await ctx.send(embed=embed)
        else:
          await ctx.send("There is no message to snipe!")
          return


    @commands.group()
    @commands.has_permissions(manage_messages = True)
    async def draw(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("thats not a valid operation")

    @draw.command()
    async def create(self, ctx, *members: str):
        
        global f
        f = list(members)
        await ctx.send("successfully created")
        global n
        n = list(members)
        

    @draw.command()
    async def pick(self, ctx, no: int):
      if not f:
        await ctx.send("u already chose everyone")
      elif len(f) < no:
        await ctx.send(f"oops,we dont have that much to pick,u can only pick {len(n)} or less")
      g = random.sample(f, k=no)
      desc=''
      
      for i in g: 
        desc+=f"{g.index(i)+1}.{i}\n"
        f.remove(i)
      emb = discord.Embed(type = "article", title="Co-op Draw", description = f"**Group**\n{desc}", timestamp = ctx.message.created_at,color=0xFFFFF)
      emb.set_footer(text=f"This group was created by {ctx.author}", icon_url=ctx.author.display_avatar)
      emb.set_thumbnail(url=ctx.guild.icon.url)
      await ctx.send(embed=emb)
      
    
    @draw.command()
    async def assign(self, ctx, no: int = 1, *choices):
      desc=''
      for i in range(len(n)):
        t = random.sample(choices, k = no)
        desc += f"{i+1}.{n[i]} - {', '.join(t[:no])}\n"

      em = discord.Embed(title="Assigned",color=0xFFFFF,timestamp = ctx.message.created_at,description=desc)
  
      em.set_footer(text=f"This was created by {ctx.author}", icon_url=ctx.author.display_avatar)  
      em.set_thumbnail(url=ctx.guild.icon.url)
      await ctx.send(embed=em)
    
    
    
    @commands.group(aliases=["co-op"])
    async def co_op(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("type z!co-op friendly/z!co-op online")

  
    
   
    @commands.command()
    async def match(self,ctx,p1,p2):
      k1 = random.choice(range(7))
      k2 = random.choice(range(7))
      await ctx.send(f"{p1} {k1}-{k2} {p2}")

    @commands.command()
    async def em(self,ctx,*,text):
      emojis=[]
      for s in text.lower():
        if s.isdecimal():
          num={'0':'zero','1':'one','2':'two',
              '3':'three','4':'four','5':'five',
              '6':'six','7':'seven','8':'eight',
              '9':'nine'}
          emojis.append(f":{num.get(s)}:")
        elif s.isalpha():
          emojis.append(f":regional_indicator_{s}:")
        else:
          emojis.append(s)
    
      await ctx.send(' '.join(emojis)) 
    
    @commands.command()
    async def ascii(self,ctx,font,*,word):
      f = Figlet(font=f'{font}')
      await ctx.send(f"```{f.renderText(word)}```")

    @commands.command(
        name='reload', description="Reload all/one of the bots cogs!"
    )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.client.unload_extension(f"cogs.{ext[:-3]}")
                            self.client.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        await self.client.unload_extension(f"cogs.{ext[:-3]}")
                        await self.client.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def toggle(self,ctx,*,command):
      command = self.client.get_command(command)

      if command is None:
        await ctx.send("cannot find a command with that name")
      
      elif ctx.command == command:
        await ctx.send("cannot disable that command")
      else:
        command.enabled = not command.enabled
        ternary = "enabled" if command.enabled else "disabled"
        await ctx.send(f"i have {ternary} {command.qualified_name}")


    @commands.command()
    async def qr(self, ctx, *msg):
      img  = qrcode.make(f"{msg}")
      img.save("qrcode.png")
      file = discord.File("qrcode.png")
      await ctx.send(file=file)

    @commands.command()
    async def yt(self,ctx,*,st: str):
      await ctx.send(f"https://www.youtube.com/results?search_query={st}")

    @commands.command()
    async def countdown(self, ctx, seconds):
      if(seconds.endswith('s')):
        second = int(seconds[0:-1])
      elif(seconds.endswith('h')):
        second = int(seconds[0:-1]) * 3600
      elif(seconds.endswith('m')):
        second = int(seconds[0:-1]) * 60
      else:
        await ctx.send("enter time in correct format(3h, 2m, 1s)")


      msg = await ctx.send(f"countdown ends <t:{math.floor(time.time() + second)}:R>", delete_after = second)
      await asyncio.sleep(second)
      await ctx.send("countdown finished", delete_after = 3)

          
# Now, we need to set up this cog somehow, and we do that by making a setup function:
async def setup(client):
  await client.add_cog(SomeCommands(client))