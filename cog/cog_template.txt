from discord.ext import commands
import discord

# intents = discord.Intents.all()
# client = commands.Bot(command_prefix='.', intents=intents)


class t(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(cl):
    cl.add_cog(t(cl))
