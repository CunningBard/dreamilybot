import time
import main
import utilities.util as util
from discord.ext import commands
import discord


class Startup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        duration = time.time() - main.start
        print("Bot is Ready")
        channel_chat_bot = self.client.get_channel(util.BotChat)
        embed = util.make_embed("Ready To Run!", "blue", f"I'm ready to do my tasks, start up took {round(duration, 2)}s")
        await channel_chat_bot.send(embed=embed)

    @commands.slash_command(description="Sends the bot's latency.")
    async def ping(self, ctx):
        await ctx.send(embed=util.make_embed("Pong!", "blue", f"Ping: {round(self.client.latency * 1000)}ms"))


def setup(cl):
    cl.add_cog(Startup(cl))
