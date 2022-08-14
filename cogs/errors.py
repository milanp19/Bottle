
import discord
from discord.ext import commands

import asyncio


import datetime



class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        
        if hasattr(ctx.command, 'on_error'):
            return

        

        if isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            await ctx.send(_message)
            return


        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, discord.errors.HTTPException):
            await ctx.send("Something went wrong.")
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'ratio')#The command has been disabled automatically since u r using it too much.')
            return
        
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You are on cooldown. Please try again in **{error.retry_after:.2f}s**")
            return

        
        if isinstance(error, discord.ext.commands.errors.NotOwner):
            await ctx.send("You are not the owner of this bot so you can't use this command")
            return

        if isinstance(error, IndexError):
            await ctx.send("Thats not a valid index")
            return

        if isinstance(error, ValueError):
            await ctx.send(f"{error}")
            return
        

        if isinstance(error, discord.ext.commands.ChannelNotFound):
            await ctx.send("Channel doesn't exist")


        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permissions to do that,pls tell an admin to give you permissions.")
            return

        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Channel not found.")
            return
        
        
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("That member doesn't exist.")
            return

        if isinstance(error, commands.MissingRole):
            await ctx.send("`You dont have the required role to do that")
        
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f"{error}")
            return

        
        if isinstance(error.original, discord.Forbidden):
            await ctx.send("I dont have permissions to do that.")
            return


        if isinstance(error, discord.NotFound):
            await ctx.send("Cant find that sorry")
            return

        if isinstance(error, asyncio.TimeoutError):
            await ctx.send("your too lazy to give me a response.Goodbye")
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'Command can not be used in Private Messages.')
                return
            except discord.HTTPException:
                await ctx.send("Something went wrong.")
        

        elif isinstance(error, commands.BadArgument):
          if ctx.command.qualified_name == 'tag list':
            await ctx.send('I could not find that member. Please try again.')
          else:
            await ctx.send("try to pass the correct argument")
            return
        else:
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(858584431714762802)
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')
            return

async def setup(client):
    await client.add_cog(CommandErrorHandler(client))