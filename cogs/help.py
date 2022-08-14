from discord import Embed
from discord.ext import commands

from dpymenus import PaginatedMenu


class MyPaginatedMenu(commands.Cog):
  def __init__(self, client):
        self.client = client

  @commands.command()
  async def help(self, ctx):
    e1 = Embed(title="Help", description="This page is for helping you guys understand the commands.", color=0xFFFFF, timestamp = ctx.message.created_at)

    e1.add_field(name="command", value="Command to try.", inline=True)#adding fields and such here.
    e1.add_field(name="help", value="This is the help command.", inline=True)
    e1.add_field(name="ban", value="Bans the user.\nmust have ban perms", inline=True)
    e1.add_field(name="kick", value="kicks the user.\nmust have kick perms", inline=True)
    e1.add_field(name="imitate", value="Imitates the given words.", inline=True)
    e1.add_field(name="mute", value="mutes a mentioned member.\nexample:\n z!mute <member> <time s/m/h/d>\nmust have mute member perms", inline=True)
    e1.add_field(name="z!iconic(s)", value="gives u a random iconic player", inline=True)
    e1.add_field(name="z!legend(s)", value="gives u a random legend player")
    e1.add_field(name='z!translate(z!tr)', value='translates the text\nto a given language\nexample:\nz!tr <lang to translate> <text>')
   
    e1.set_thumbnail(url = ctx.guild.icon_url)
    e1.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author}")
      


    e2 =  Embed(title="Help", description="This page is for helping you guys understand the commands.", color=0xFFFFF, timestamp = ctx.message.created_at)
    e2.add_field(name='z!work', value='earn money by working\nusage:type z!work')
    e2.add_field(name='z!balance', value='check your balance\nusage:type z!balance')
    e2.add_field(name='Fun commands', value='z!pro,z!noob,z!imitate (text),\nz!luck,z!rickroll,z!members\n(do check them out)')
    e2.add_field(name="z!guildid", value="to get server id\nmust have admin perms")
    e2.add_field(name='clear', value="cear messages\nusage: z!clear <no of messages to clear>\nmust have manage messages perms")
    e2.add_field(name='addrole', value="adds specified role\nmust have admin perms") 
    e2.add_field(name="z!members", value='gives the number of\nmembers in the server')
    e2.add_field(name='z!channel', value='gives channel id\nmust have admin perms')
    e2.add_field(name='z!nickname', value='allows u to change name of members\nmust have manage nicknames perms\nusage: z!nickname <member_mention> <nickname>')
      

    e2.set_thumbnail(url = ctx.guild.icon_url)
    e2.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author}")
      

    e3 = Embed(title='Page 3', description='Third page test!')
    e3.add_field(name='inspire me', value='just type as it is\n and get inspired')
    e3.add_field(name='embed', value='allows you to send embed of urchoice\n    this command\n    only for me <:help:832637479726219276>')
    e3.add_field(name='z!unmute', value='unmutes the member\nmust have admin perms')
      
    e3.set_thumbnail(url = ctx.guild.icon.url)
    e3.set_footer(icon_url = ctx.author.avatar_url, text = f"requested by {ctx.author}")


    cancel = Embed(title='Cancel Page', description='Cancel page test.')
    cancel.add_field(name='Example E', value='Example F')

    timeout = Embed(title='Timeout Page', description='Timeout page test.')
    timeout.add_field(name='Example E', value='Example F')

    menu = PaginatedMenu(ctx)
    menu.add_pages([e1, e2, e3])
    menu.buttons(["👈", "⏹️", "👉"])
    menu.set_timeout(20)
      
    await menu.open()
      

      
        # You can also do fluent-style chaining on the menu methods; similar to a discord.py Embed. For example...
        #
        # menu = (PaginatedMenu(ctx)
        #         .set_timeout(5)
        #         .add_pages([page1, page2, page3, page4])
        #         .show_skip_buttons()
        #         .hide_cancel_button()
        #         .set_destination(ctx.author)
        #         )
        # await menu.open()
        #
        # ...or...
        #
        # menu = PaginatedMenu(ctx).add_pages([e1, e2, e3]).set_cancel_page(cancel).set_timeout_page(timeout).set_timeout(20)
        # await menu.open()
      



async def setup(client):
  await client.add_cog(MyPaginatedMenu(client))