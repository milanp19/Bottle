import discord
from discord.ext import commands, tasks


class BackgroundTasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.check_users.start()

    def cog_unload(self) -> None:
        self.check_users.stop()


    @tasks.loop(seconds=7)
    async def check_users(self):
        online = 0
        offline = 0
        idle = 0
        dnd = 0

        for member in self.client.guilds[0].members:
            if member.status == discord.Status.online:
                online += 1
            if member.status == discord.Status.offline:
                offline += 1
            if member.status == discord.Status.idle:
                idle += 1
            if member.status == discord.Status.dnd:
                dnd += 1
            info = {
                "online": online,
                "offline": offline,
                "idle": idle,
                "dnd": dnd,
            }

            channel = self.client.get_channel(1041065970397089802)

            await channel.send(info)
    



async def setup(client):
    await client.add_cog(BackgroundTasks(client))