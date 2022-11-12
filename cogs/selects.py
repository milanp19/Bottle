import discord
from discord.ext import commands
from discord import app_commands

class FavouriteGames(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="GTA",
                value="GTA",
            ),
            discord.SelectOption(
                label="COD",
                value="COD",
            ),
            discord.SelectOption(
                label="Genshin Impact",
                value="Genshin Impact",
            ),
        ]
        super().__init__(options = options, placeholder = "What do you want to play?", max_values = 2)
    async def callback(self, interaction: discord.Interaction):
        await self.view.respond_to_answer2(interaction, self.values)

class SurveyView(discord.ui.View):
    answer1 = None
    answer2 = None


    @discord.ui.select(
        placeholder = "What is your age?",
        options = [
            discord.SelectOption(label = "1", value = 1),
            discord.SelectOption(label = "2", value = 2),
            discord.SelectOption(label = "3", value = 3),
        ]
    )
    async def select_age(self, interaction: discord.Interaction, select_item: discord.ui.Select):
        self.answer1 = select_item.values
        self.children[0].disabled = True
        game_select = FavouriteGames()
        self.add_item(game_select)
        await interaction.message.edit(view = self)
        await interaction.response.defer()

    
    async def respond_to_answer2(self, interaction: discord.Interaction, choices):
        self.answer2 = choices
        self.children[1].disabled = True
        await interaction.message.edit(view = self)
        await interaction.response.defer()
        self.stop()


class Select(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command()
    async def choose(self, ctx):
        view = SurveyView()
        await ctx.send(view = view)  


        await view.wait()

        results = {
            "d1": view.answer1,
            "d2": view.answer2,
        }

        await ctx.send(f"{results}")


async def setup(client):
    await client.add_cog(Select(client))