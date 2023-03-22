from discord.ext import commands
import discord
import asyncio

class Moderation(commands.Cog):
  def __init__(self,client):
    self.client=client

  @commands.command(aliases=["comall"])
  async def commandsall(self,ctx):
    k = len(self.client.all_commands)
    em = discord.Embed(title="No of commands",description=f"`total commands`: {k}",color=ctx.author.color)
    await ctx.send(embed = em)

  @commands.command(name="blacklist",aliases=["b"])
  @commands.is_owner()
  async def blacklist(self, ctx, targets: commands.Greedy[discord.Member]):
    if not targets:
      await ctx.send("No targets specified.")

    else:
      self.client.blacklisted.extend([t.id for t in targets])
      with open("./data/blacklist.txt", "w", encoding="utf-8") as f:
        f.writelines([f"{item}\n" for item in self.client.blacklisted])
      await ctx.send(f"i have blacklisted mentioned user(s)")

  @commands.command(name="unblacklist", aliases=["ub"])
  @commands.is_owner()
  async def delban_command(self, ctx, targets: commands.Greedy[discord.Member]):
    if not targets:
      await ctx.send("No targets specified.")

    else:
      for target in targets:
        self.client.blacklisted.remove(target.id)
      with open("./data/blacklist.txt", "w", encoding="utf-8") as f:
        f.writelines([f"{item}\n" for item in self.client.blacklisted])
      await ctx.send("i have whitelisted mentioned user(s)")
   
  
  @commands.command(name='kick')
  @commands.has_permissions(manage_roles = True)
  #@commands.has_permissions(administrator=True)
  async def kick(self, ctx, user: discord.Member,*,reason):
    await user.kick(reason=reason)
    await ctx.send(f'{user} kicked for {reason}')


  @commands.command(name='ban')
  #@commands.has_permissions(administrator=True)
  @commands.has_permissions(manage_roles = True)
  async def ban(self, ctx, user: discord.Member,*,reason):
    await user.ban(reason=reason)
    await ctx.send(f'{user} banned for {reason}')  

  @commands.command(name = 'mute', description="Mutes the specified user.")
  #@commands.is_owner()
  #@commands.has_permissions(administrator=True)
  # @commands.has_permissions(kick_members = True)
  async def mute(self, ctx, member: discord.Member, time1=None, *, reason=None):
      guild = ctx.guild
      mutedRole = discord.utils.get(guild.roles, name="Muted")

      if not mutedRole:
          mutedRole = await guild.create_role(name="Muted")

          for channel in guild.channels:
              await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
      if not time1:
        await member.add_roles(mutedRole, reason=reason)
        await ctx.send(f"muted {member.mention} indefinitely\nreason: {reason}")
      else:
        d = time1[-1]        
        t = int(time1[:-1])
        await member.add_roles(mutedRole, reason=reason)
        if d == "s":
          await ctx.send(f"Muted {member.mention} for {t} second(s) \nreason: {reason}")
          #await member.send(f"You were muted in the server {guild.name} for {t} second(s) \nreason: {reason}")
          await asyncio.sleep(t)

        if d == "m":
          await ctx.send(f"Muted {member.mention} for {t} minute(s) \nreason: {reason}")
          #await member.send(f"You were muted in the server {guild.name} for {t} minute(s) \nreason: {reason}")
          await asyncio.sleep(t*60)

        if d == "h":
          await ctx.send(f"Muted {member.mention} for {t} hour(s) \nreason: {reason}")
          #await member.send(f"You were muted in the server {guild.name} for {t} hour(s) \nreason: {reason}")
          await asyncio.sleep(t*60*60)

        if d == "d":
          await ctx.send(f"Muted {member.mention} for {t} day(s) \nreason: {reason}")
          #await member.send(f"You were muted in the server {guild.name} for {t} day(s) \nreason: {reason}")
          await asyncio.sleep(t*60*60*24)

        

        await member.remove_roles(mutedRole)
        await ctx.send(f"{member.mention} is unmuted after {t}{d}")


  @commands.command(name='unmute', description="Unmutes a specified user.")
  #@commands.is_owner()
  # @commands.has_permissions(kick_members = True)
  #@commands.has_permissions(administrator=True)
  #@commands.has_permissions(manage_roles = True)
  async def unmute(self, ctx, member1: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member1.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member1.mention}")
    #await member1.send(f"You were unmuted in the server {ctx.guild.name}")

  
  


async def setup(client):
  await client.add_cog(Moderation(client))



#http://api.wolframalpha.com/v1/simple?appid=5322Q6-9U3UYGATLR&i={query}%3F
