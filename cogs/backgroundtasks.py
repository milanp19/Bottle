import discord
from discord.ext import commands, tasks
import asyncio

class BackgroundTasks(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.check_users.start()
        self.ctx = None
        self.remind.add_exception_type(Exception)
        self.message = ""


    def cog_unload(self) -> None:
        self.remind.stop()


    @tasks.loop(seconds=7)
    async def remind(self):
        # online = 0
        # offline = 0
        # idle = 0
        # dnd = 0
        
        
        # for member in self.client.guilds[0].members:
        #     if member.status == discord.Status.online:
        #         online += 1
        #     if member.status == discord.Status.offline:
        #         offline += 1
        #     if member.status == discord.Status.idle:
        #         idle += 1
        #     if member.status == discord.Status.dnd:
        #         dnd += 1
        

        # info = {
        #     "online": online,
        #     "offline": offline,
        #     "idle": idle,
        #     "dnd": dnd,
        # }
        
        # print(info)
        if(self.remind.current_loop == 0):
            return
        await self.ctx.send(f"{self.ctx.author.mention}, Your Event {self.message} is now happening")
        self.stop()


    @commands.command()
    async def start(self, ctx):
        self.remind.start() 


    @commands.command()
    async def cancel(self, ctx):
        self.remind.cancel() 


    @commands.command()
    async def reminder(self, ctx, time: str, *, message):
        self.ctx = ctx
        self.message = message
        msg = None
        time_after = int(''.join(time[:-1]))
        hmd = time[:][-1].lower()

        if time_after <= 10 and hmd == "s":
            await ctx.send("put reminder for something more than 10 seconds")
            return
        elif hmd == "m": 
            msg = "minute(s)"
            self.remind.change_interval(minutes=time_after) 
        
        elif hmd == "s": 
            msg = "second(s)"
            self.remind.change_interval(seconds=time_after) 

        elif hmd == "h":
            msg = "hours(s)"
            self.remind.change_interval(hours=time_after) 
        else:
            await ctx.send("invalid time format, pls use the time format like this -> (3s, 3d, 3h)")

        embed = discord.Embed(
            title = message,
            description = f"I will notify you after {time_after} {msg}"
            )


        await ctx.send(embed = embed)
        # self.remind.start()
        asyncio.create_task(self.remind())
        # await asyncio.sleep(time_after)


    @remind.before_loop
    async def before_remind(self):
        await self.client.wait_until_ready()
        print("Before starting loop")



    @remind.after_loop
    async def after_remind(self):
        print("After stopping loop")




async def setup(client):
    await client.add_cog(BackgroundTasks(client))

    