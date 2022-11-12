import discord
from discord.ext import commands
from discord import app_commands

class SimpleView(discord.ui.View):

    foo: bool = None

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True

        await self.message.edit(view = self) 


    async def on_timeout(self) -> None:
        await self.message.channel.send("Timed Out")
        await self.disable_all_items()
    
    
    @discord.ui.button(label = "Hello", style = discord.ButtonStyle.success)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("World")
        self.foo = True
        self.stop()

    @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelling")
        self.foo = False
        self.stop()

    
class Buttons(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def button(self, ctx):
        view = SimpleView(timeout = 3)
        # button = discord.ui.Button(label = "Click Me")
        # view.add_item(button)
        message = await ctx.send(view = view)
        view.message = message
        await view.wait()
        await view.disable_all_items()

        if view.foo is None:
            await ctx.send("Error")
        elif view.foo is True:
            await ctx.send("ok")
        else:
            await ctx.send("cancel")



async def setup(client):
    await client.add_cog(Buttons(client))