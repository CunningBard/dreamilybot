import discord


def make_embed(title, color, desc):
    color = color.lower()
    if color == "blue":
        return discord.Embed(title=title, description=desc, color=discord.Color.blue())
    elif color == "red":
        return discord.Embed(title=title, description=desc, color=discord.Color.red())
    elif color == "green":
        return discord.Embed(title=title, description=desc, color=discord.Color.green())
    elif color == "yellow":
        return discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(255, 255, 0))
    elif color == "black":
        return discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(0, 0, 0))
    elif color == "light-blue":
        return discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(0, 255, 255))
    elif color == "orange":
        return discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(255, 170, 0))
    else:
        return discord.Embed(title=title, description=desc, color=discord.Color.from_rgb(255, 255, 255))


BotChat = 988469746968174633