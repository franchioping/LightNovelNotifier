import discord
import json
import data_file
from api import light_novel, light_novel_api
import time
import asyncio

from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

data: data_file.DataFile
ln_api: light_novel_api.LightNovelApi

config: dict

with open("config.json", "r") as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)


def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id

    return commands.check(predicate)


@bot.event
async def on_ready():
    global data, ln_api
    data = data_file.DataFile()
    ln_api = light_novel_api.LightNovelApi()
    print("Booting up your system")
    print("I am running on " + bot.user.name)
    print("With the ID: " + str(bot.user.id))

    for guild in [bot.get_guild(g_id) for g_id in data.get_guild_id_list()]:
        if data.get_guild_select_message_id(guild) < 0:
            msg = await guild.get_channel(data.get_guild_select_channel_id(guild)).send("Chose LightNovels Here:")
            data.set_guild_select_message_id(guild, msg.id)

    check_new_chapters.start()
    print("Init Done!")


@bot.command()
@commands.check_any(is_guild_owner())
async def get_data(ctx: discord.ext.commands.Context):
    await ctx.send(json.dumps(data.data, indent=2, ensure_ascii=False))


@bot.command()
@commands.check_any(is_guild_owner())
async def add_ln(ctx: discord.ext.commands.Context, *args):
    if len(args) != 2:
        await ctx.send("Wrong Usage")
        return

    ln_name: str = args[0]
    ln_emoji: str = args[1]

    category = discord.utils.get(ctx.guild.categories, id=data.get_guild_ln_category_id(ctx.guild))

    everyone = ctx.guild.default_role
    ln = light_novel.LightNovel(ln_name, ln_api, emoji=ln_emoji)
    name = ln.get_name()

    channel = await ctx.guild.create_text_channel(name, category=category)
    notification_role = await ctx.guild.create_role(name=name)
    await channel.set_permissions(everyone,
                                  overwrite=discord.PermissionOverwrite(send_messages=False, view_channel=False))
    await channel.set_permissions(notification_role, overwrite=discord.PermissionOverwrite(view_channel=True))

    ln.channel_id = channel.id
    ln.role_id = notification_role.id

    data.add_ln(ctx.guild, ln)

    select_channel = ctx.guild.get_channel(data.get_guild_select_channel_id(ctx.guild))
    select_message = await select_channel.fetch_message(data.get_guild_select_message_id(ctx.guild))
    content = select_message.content
    new_content = content + "\n" + name + " - " + ln_emoji
    await select_message.edit(content=new_content)

    await ctx.send(f"/reactionrole add message_id:{select_message.id} emoji:{ln_emoji} role:{notification_role.mention}")


@tasks.loop(seconds=int(config["delay"]))
async def check_new_chapters():
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    for guild in [bot.get_guild(g_id) for g_id in data.get_guild_id_list()]:

        for ln in [light_novel.LightNovel.from_dict(ln_dict, ln_api) for ln_dict in data.get_lns(guild)]:
            await asyncio.sleep(.5)

            latest_chap = ln.get_latest_chap()

            if latest_chap != ln.latest_chap:
                ln.update_latest_chap()
                role = guild.get_role(ln.role_id)

                await guild.get_channel(ln.channel_id).send(
                    embed=ln.get_embed(time_str, latest_chap),
                    content=role.mention, allowed_mentions=discord.AllowedMentions(everyone=True))

                data.update_ln(guild, ln)
                data._save()


bot.run(config["token"])
