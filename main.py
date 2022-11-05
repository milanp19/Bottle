import discord
from discord.ext import commands
import os
import random
import json
import googletrans
import asyncio
import requests
from bbs import bb_list
import aiohttp 
import io
from playstyles import playstyles

from dotenv import load_dotenv

load_dotenv()


def get_prefix(client,message):

  with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

  return prefixes[str(message.guild.id)]
  

#client = discord.Client()#declaring what the client is.
# , intents = discord.Intents.all()
client = commands.Bot(command_prefix=get_prefix, intents = discord.Intents.all(), case_insensitive = True)#Makes the client prefix.
client.blacklisted = []

client.remove_command('help')#Removes the auto help command as it can be buggy.

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def owneradmin():
  async def predicate(ctx):
    return ctx.author.id == 538282588846948362 or ctx.author.guild_permissions.kick_members or ctx.author.guild_permissions.manage_roles
  return commands.check(predicate)



@client.event
async def on_ready():
  
  print("client joined/Updated successfully!")
  with open("./data/blacklist.txt", "r", encoding="utf-8") as f:
    client.blacklisted = [int(line.strip()) for line in f.readlines()]


  await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name='COSMO'))
  
@client.event
async def on_guild_join(guild):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] = ">"

  with open("prefixes.json", "w") as f:
    json.dump(prefixes,f)

@client.event
async def on_message(msg):
  
  if msg.author.id == client.user.id:
    return 
  try:
    if msg.mentions[0] == client.user:
      with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

      pre = prefixes[str(msg.guild.id)] 

      await msg.channel.send(f"My prefix for this server is {pre}")

  except:
    pass
 
  if msg.content.startswith('inspire me'):
    quote = get_quote()
    await msg.author.send(quote)
  
  if msg.content.startswith(':') and msg.content.endswith(':'):
    client.delete_message(msg)
  

  ctx = await client.get_context(msg)
  if ctx.command is not None:
    if msg.author.id in client.blacklisted: 
      await msg.channel.send("you are banned from using commands")
      return


  await client.process_commands(msg)  

@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):

  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)

  prefixes[str(ctx.guild.id)] = prefix

  with open("prefixes.json", "w") as f:
    json.dump(prefixes,f)    

  await ctx.send(f"The prefix was changed to {prefix}")


     
@client.command()
@commands.is_owner()
async def leaveguild(ctx, id: int):
  to_leave = client.get_guild(id)
  await to_leave.leave()
  await ctx.send("left that server successfully")

@client.command()
@commands.is_owner()
async def logout(ctx):
  await client.logout()




@client.command()
@commands.is_owner()
async def servers(ctx):
  k = []
  g=''
  for i in client.guilds:
    k.append(i.name)
  for i in range(1):
    g+=', '.join(k)
  await ctx.send(g)  
  
@client.command()
@commands.is_owner()
async def serversinfo(ctx):
    k = client.guilds 
    await ctx.send(str(k))

@client.command()
#@commands.has_permissions(administrator=True)
async def guildid(ctx):
  g = str(ctx.guild.id)
  await ctx.send(g)

@client.command()
@commands.is_owner()
async def triggered(ctx, member: discord.Member=None):
    if not member: # if no member is mentioned
        member = ctx.author # the user who ran the command will be the member
        
    async with aiohttp.ClientSession() as wastedSession:
        async with wastedSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage: # get users avatar as png with 1024 size
            imageData = io.BytesIO(await wastedImage.read()) # read the image/bytes
            
            await wastedSession.close() # closing the session and;
            
            await ctx.reply(file=discord.File(imageData, 'triggered.gif')) # sending the file
            
@client.command()
async def binary(ctx, *, text: str = None):
  await ctx.message.delete()
  binary_url = f"https://some-random-api.ml/binary?text={text}"
  if text == None:
    await ctx.send("please provide text to convert into binary")
  async with aiohttp.ClientSession() as bin:
    response = await bin.get(binary_url)
    k = await response.json()
    await ctx.send(k["binary"])


@client.command(aliases = ["blackball"])
@commands.cooldown(1,40,commands.BucketType.user)
async def bb(ctx):
  urls="https://media.giphy.com/media/a3h3S2CVPzpyzqBtwX/giphy-downsized.gif"
  a = await ctx.send(urls)
  await asyncio.sleep(8)
  await a.delete()
   
  r = random.choice(bb_list)
  embed = discord.Embed(title = f"Wow {ctx.author.name}, you packed:", description="**‎‎‎‎\u200b\n\u200b‎\n\u200b\n{}** \n (Blackball)".format(r), color=0xFFFFF, timestamp = ctx.message.created_at)

  
  embed.set_thumbnail(url = urls)
  embed.set_footer(icon_url = ctx.author.avatar.url, text = f"packed by {ctx.author}")
 
  await ctx.send(embed=embed)  
  await ctx.send("**Good Pull or scripted?** <:help:843403016379826186>")

@client.command()
async def cat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      dogjson = await request.json()
      # This time we'll get the fact request as well!
      request2 = await session.get('https://some-random-api.ml/facts/cat')
      factjson = await request2.json()

   embed = discord.Embed(title="CATS!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   embed.set_footer(text=factjson['fact'])
   await ctx.send(embed=embed)  

@client.command(aliases = ["tr"])
async def translate(ctx, lang, *args):
  lang = lang.lower()
  if lang == "chinese":
    lang = "zh-cn"
  elif lang not in googletrans.LANGUAGES and lang not in googletrans.LANGCODES:
    await ctx.send("invalid language to translate text to")
  
  text = ' '.join(args)
  translator = googletrans.Translator()
  text_translated = translator.translate(text, dest=lang).text 
  await ctx.send(text_translated)


@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int):
  await ctx.channel.purge(limit = amount+1)

@client.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, role: discord.Role, member: discord.Member):
  await member.add_roles(role)

@client.command()
@commands.has_permissions(administrator=True)
async def removerole(ctx, role: discord.Role, member: discord.Member):
  await member.remove_roles(role)

@client.event
async def on_command_error(ctx, error):
  print(f'{error}')


@client.command()
async def imitate(ctx,*, mssg=None):
  if mssg == None:
    await ctx.send('Put the message you need in.')
  else:
    await ctx.send(f'{mssg}',allowed_mentions=discord.AllowedMentions(everyone=False))
  await ctx.message.delete()  


@client.command()
@commands.has_permissions(administrator=True)
async def channel(ctx, chnl: discord.TextChannel = None):
  if chnl == None:
    await ctx.send(ctx.channel.id)
  else:  
    await ctx.send(chnl.id)

@client.command()
async def luck(ctx):
  rand1 = random.choice(range(0,100))
  await ctx.send(f"{rand1}%")

@client.command()
async def pro(ctx):
  rand2 = random.choice(range(0,100))
  await ctx.send(f"{rand2}%")


@client.command()
@commands.is_owner()
#@commands.has_permissions(manage_nicknames=True)
async def nickname(ctx, user: discord.Member,*,nick):
  await user.edit(nick=nick)

@client.command()
async def noob(ctx, user: discord.Member = None):
  rand3 = random.choice(range(0,100))
  if user == None:
    await ctx.reply(f"you are {rand3}% noob")
  else:
    await ctx.send(f"{user.mention} is {rand3}% noob")

@client.command()
async def script(ctx):
  rand4 = random.choice(range(0,100))
  await ctx.send(f"{rand4}%")    


'''@client.command()
@commands.cooldown(1,10,commands.BucketType.user)
async def love(ctx, user1: discord.Member, user2: discord.Member):
  rand5 = random.choice(range(0,100))
  await ctx.send(f"{rand5}% love between {user1.name} and {user2.name}")'''


@client.command()
@commands.cooldown(1,10,commands.BucketType.user)
async def whale(ctx, user: discord.Member = None):
  rand6 = random.choice(range(0,100))
  if user == None:
    await ctx.reply(f"you are {rand6}% whale 🐋")
  
  else:
    await ctx.send(f"{user.mention} is {rand6}% whale 🐋")


@client.command()
async def members(ctx):
  members = str(ctx.guild.member_count)
  await ctx.send(f"No: of members: {members}")


 

@client.command()
@commands.cooldown(1,7,commands.BucketType.user)
@owneradmin()
#@commands.has_permissions(kick_members = True)
async def embed(ctx, desc, ch: discord.TextChannel = None):
  embed1 = discord.Embed(description=f"{desc}", color=0xFFFFF)
  if ch == None:
    await ctx.send(embed=embed1)
  else:
    k=client.get_channel(ch.id)
    await k.send(embed=embed1)


@client.command(aliases=["ps"])
async def playstyle(ctx,*,p = None):
  if p == None:
    embed = discord.Embed(title="Playstyle", description="A Help menu for playstyles", color=000000)  
    j = playstyles.keys()
    for i in j:
      embed.add_field(name=f"{i}", value="\u200b", inline=True)
    embed.set_footer(text = "Type z!playstyle <name of playstyle> to know more about a playstyle")

  else:
    embed = discord.Embed(title=f"{p.upper()}", description=f"{playstyles[p][0]}\n\u200b\n{playstyles[p][1]}", color=0xFFFFF, timestamp = ctx.message.created_at)
    embed.set_footer(icon_url = ctx.author.avatar.url, text = f"requested by {ctx.author}")

  await ctx.send(embed=embed)



@client.command()
async def peshelp(ctx):  
  embed = discord.Embed(title="PES", description = "PES commands help", color = 0xFFFFF )
  embed.add_field(name="z!iconic(s)", value="gives u a random iconic player", inline=True)
  embed.add_field(name="z!legend(s)", value="gives u a random legend player")
  embed.add_field(name="z!bb or z!blackball", value="gives u a random blackball player", inline=True)
  embed.add_field(name="z!setid", value="stores ur pes id, so no need to \nopen PES mobile to get ur ID\nusage: z!setid 123456789 ", inline=True)
  embed.add_field(name="z!getid", value="displays your stored PES ID\nusage: z!getid (shows your PES ID)\nzgetid <mention a member> (gets you the mentioned member's stored ID)\neg: z!getid @COSMO", inline=True)

  await ctx.send(embed=embed)

@client.command()
async def commands(ctx):
  emb = discord.Embed(description = f"Total commands: `{len(client.commands)}`", color = ctx.author.colour, timestamp = ctx.message.created_at)
  emb.set_footer(icon_url = ctx.author.avatar.url, text = f"requested by {ctx.author}")
  await ctx.send(embed = emb)
  


async def load_extensions():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      await client.load_extension(f'cogs.{filename[:-3]}')


#client.run(os.getenv('TOKEN'))

async def main():
    async with client:
        await load_extensions()
        await client.start(os.getenv('TOKEN'))

asyncio.run(main())