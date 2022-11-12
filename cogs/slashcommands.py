import discord
from discord import app_commands
from discord.ext import commands
import typing


class SlashCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @app_commands.command(description="welcome", name="hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("hi")
    

    @app_commands.command(description="Welcome", name="say")
    @app_commands.describe(thing_to_say = "What should i say")
    async def say(self, interaction: discord.Interaction, *,thing_to_say: str):
        await interaction.response.send_message(f"hi, you said {thing_to_say}")


    async def animals_autocomplete(
        self, interaction: discord.Interaction, 
        current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for animal_choice in ['Cow', 'Deer', 'Lion', 'Tiger', 'Hyena']:
            if current.lower() in animal_choice.lower():
                data.append(app_commands.Choice(name=animal_choice, value=animal_choice))
        return data


    @app_commands.command()
    @app_commands.autocomplete(item=animals_autocomplete)
    async def animals(self, interaction: discord.Interaction, item: str):
        await interaction.response.send_message(f"{item}", ephemeral = True)


async def setup(client):
    await client.add_cog(SlashCommands(client))