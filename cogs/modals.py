import discord
from discord.ext import commands
from discord import app_commands

class Feedback(discord.ui.Modal, title = "Send me your feedback"):
    fb_title = discord.ui.TextInput(
        style = discord.TextStyle.short,
        label = "Title",
        required = False,
        placeholder = "Give Your Feedback Some Title"

    )


    message = discord.ui.TextInput(
        style = discord.TextStyle.long,
        label = "Message",
        required = False,
        max_length = 500,
        placeholder = "Give Us Your Message"

    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = self.client.get_channel(1041025648841474078)
        embed = discord.Embed(title = "New Feedback", description = f"{self.message.value}", color = discord.Color.yellow())
        embed.set_author(name = self.user.nick)
        await channel.send(embed = embed)
        await interaction.response.send_message("We recieved your feedback, Thank You", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error):
        pass


class Modal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="feedback", description= "Give us your feedback")
    async def feedback(self, interaction: discord.Interaction):
        feedback_modal = Feedback()
        feedback_modal.user = interaction.user
        feedback_modal.client = self.client
        await interaction.response.send_modal(feedback_modal)


    


async def setup(client):
    await client.add_cog(Modal(client))