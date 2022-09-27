import os
import time
import discord
import secrets_folder.secret as sc
import utilities.util.data as data
# from runner import keep_alive
from discord.ext import commands

start = time.time()
wait_time = 10

intents = discord.Intents.default()
bot = discord.Bot(command_prefix="?", intents=intents)

last_reload = None

database = data.Database("dynamic_files/data.txt", sc.database_password)
database.import_content()


async def load_cog(ctx, extension):
    directory = os.listdir("cog")

    if extension + ".py" in directory:
        try:
            bot.load_extension(f"cog.{extension}")
            await ctx.send(f"cog {extension} has been loaded")
        except discord.errors.ExtensionFailed:
            await ctx.send(f"cog {extension} has already been loaded or couldnt be loaded")
    else:
        await ctx.send(f"'{extension}' isn't a cog")


async def unload_cog(ctx, extension):
    directory = os.listdir("cog")

    if extension + ".py" in directory:
        try:
            bot.unload_extension(f"cog.{extension}")
            await ctx.send(f"cog {extension} has been unloaded")
        except discord.errors.ExtensionAlreadyLoaded:
            await ctx.send(f"cog {extension} has already been unloaded or couldnt be unloaded")
    else:
        await ctx.send(f"'{extension}' isn't a cog")


@bot.slash_command()
@commands.has_any_role("Owner", "Senior Moderator")
async def load(ctx, extension):
    await load_cog(ctx, extension)


@bot.slash_command()
@commands.has_any_role("Owner", "Senior Moderator")
async def unload(ctx, extension):
    await unload_cog(ctx, extension)


@bot.slash_command()
@commands.has_any_role("Owner", "Senior Moderator")
async def load_all(ctx):
    for file in os.listdir("cog"):
        if file.endswith(".py"):
            file = file[:-3]
            await load_cog(ctx, file)


@bot.slash_command()
@commands.has_any_role("Owner", "Senior Moderator")
async def unload_all(ctx):
    for file in os.listdir("cog"):
        if file.endswith(".py"):
            file = file[:-3]
            await unload_cog(ctx, file)


@bot.slash_command()
@commands.has_any_role("Owner", "Senior Moderator")
async def reload_all(ctx):
    for file in os.listdir("cog"):
        if file.endswith(".py"):
            file = file[:-3]
            await unload_cog(ctx, file)
            await load_cog(ctx, file)


@bot.slash_command()
@commands.has_any_role("Owner", "Senior Moderator")
async def reload(ctx, extension=""):
    global last_reload
    if not extension:
        if last_reload:
            extension = last_reload
    last_reload = extension
    await unload_cog(ctx, extension)
    await load_cog(ctx, extension)


for _file in os.listdir("cog"):
    if _file.endswith(".py"):
        bot.load_extension(f"cog.{_file[:-3]}")

# keep_alive()
bot.run(sc.bot_token)
