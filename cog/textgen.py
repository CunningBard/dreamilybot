import time

from discord.ext import commands
import utilities.dreamily as drm
import main as mn
import discord

# intents = discord.Intents.all()
# client = commands.Bot(command_prefix='.', intents=intents)


class TextGen(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(description="generate text using dreamily")
    async def generate(self, ctx, *, text=""):
        if not mn.database.has(ctx.author.id):
            mn.database.new_user(ctx.author.id)
        person = mn.database.get(ctx.author.id)
        time_since_last = time.time() - person.last_use
        if time_since_last < mn.wait_time:
            await ctx.respond(f"please wait for {round(mn.wait_time - time_since_last, 4)} more seconds")
            return
        person.last_use = time.time()
        person.command_use_times += 1
        
        interaction = await ctx.respond("Generating..")
        res = await drm.default_dream(text)
        person.last_story = text + res
        person.last_input = text
        
        await interaction.edit_original_message(content=text + res)

    @commands.slash_command(description="dev tool, doesnt generate text")
    async def dev_generate(self, ctx, *, text=""):
        if not mn.database.has(ctx.author.id):
            mn.database.new_user(ctx.author.id)
        person = mn.database.get(ctx.author.id)
        time_since_last = time.time() - person.last_use
        if time_since_last < mn.wait_time:
            await ctx.respond(f"please wait for {round(mn.wait_time - time_since_last, 4)} more seconds")
            return

        now = time.time()

        interaction = await ctx.respond("Generating..")
        res = "lorem imps-um"
        # res = await drm.default_dream(text)
        await interaction.edit_original_message(content=text + res + f"\n\ntook: {round(time.time() - now, 2)}")


    @commands.slash_command(description="didn't like what dreamily gave? regenerate now!")
    async def regenerate(self, ctx):
        if not mn.database.has(ctx.author.id):
            await ctx.respond("you dont have any previous inputs, do / generate instead 1")
            return
        person = mn.database.get(ctx.author.id)
        if not person.last_story:
            await ctx.respond("you dont have any previous inputs, do / generate instead 2")
            return
        time_since_last = time.time() - person.last_use
        if time_since_last < mn.wait_time:
            await ctx.respond(f"please wait for {round(mn.wait_time - time_since_last, 4)} more seconds")
            return
        person.last_use = time.time()
        person.command_use_times += 1

        last_input = person.last_input
        interaction = await ctx.respond("Generating..")
        res = await drm.default_dream(last_input)
        person.last_story = last_input + res
        
        await interaction.edit_original_message(content= last_input + res)

    @commands.slash_command(name="continue", description="Continue last story, Use last story as new input for generate")
    async def continuee(self, ctx):
        if not mn.database.has(ctx.author.id):
            await ctx.respond("you dont have any previous stories, do / generate instead 1")
            return
        person = mn.database.get(ctx.author.id)
        if not person.last_story:
            await ctx.respond("you dont have any previous stories, do / generate instead 2")
            return
        time_since_last = time.time() - person.last_use
        if time_since_last < mn.wait_time:
            await ctx.respond(f"please wait for {round(mn.wait_time - time_since_last, 4)} more seconds")
            return
        person.last_use = time.time()
        person.command_use_times += 1

        last_story = person.last_story
        interaction = await ctx.respond("Generating..")
        res = await drm.default_dream(last_story)
        person.last_story = last_story + res
        
        await interaction.edit_original_message(content= last_story + res)

    @commands.slash_command(description="Shows the current db")
    @commands.has_any_role("Owner", "Senior Moderator")
    async def db(self, ctx):
        await ctx.respond(mn.database.data)

    @commands.slash_command(description="forcefully write the db to the data.txt")
    @commands.has_any_role("Owner", "Senior Moderator")
    async def force_export(self, ctx):
        mn.database.export_content()
        await ctx.respond("exported")

    @commands.slash_command(description="forcefully read the db from the data.txt")
    @commands.has_any_role("Owner", "Senior Moderator")
    async def force_import(self, ctx):
        mn.database.import_content()
        await ctx.respond("imported")

    @commands.slash_command(description="exports and imports")
    @commands.has_any_role("Owner", "Senior Moderator")
    async def force_reload(self, ctx):
        mn.database.reload()
        await ctx.respond("reloaded")


def setup(cl):
    cl.add_cog(TextGen(cl))
