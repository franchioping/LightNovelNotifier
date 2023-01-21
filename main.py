import discord
import json
import data_file
from api import light_novel, light_novel_api

from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

data = data_file.DataFile()
ln_api = light_novel_api.LightNovelApi()

config: dict

with open("config.json", "r") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


@bot.event
async def on_ready():
    print("Booting up your system")
    print("I am running on " + bot.user.name)
    print("With the ID: " + str(bot.user.id))


@bot.command()
async def add_ln(ctx: discord.ext.commands.Context, *args):
    if len(args) != 2:
        await ctx.send("Wrong Usage")
        return

    ln_name: str = args[0]
    ln_emoji: str = args[1]

    ln = light_novel.LightNovel(ln_name, ln_api, emoji=ln_emoji)
    data.add_ln(ctx.guild, ln)
    await ctx.send("Done!")


bot.run(config["token"])
