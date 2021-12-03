import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)

bot_description = ""
intents = discord.Intents.default()
AuditorBot = commands.Bot(command_prefix='!', description=bot_description, intents=intents)


@AuditorBot.event
async def on_ready():
    print("Logged on as {}".format(AuditorBot.user))


@AuditorBot.event
async def on_guild_join(guild):
    g_channel = discord.utils.find(lambda x: x.name == 'general', guild.text_channels)
    if g_channel and g_channel.permissions_for(guild.me).send_messages:
        await g_channel.send("Hello!")


# @AuditorBot.command()
# async def athan(ctx: commands.Context, address: str):
#     try:
#         city, country = await get_location(address)
#     except ValueError as e:
#         await ctx.send(str(e))
#         return
#     url = "http://api.aladhan.com/v1/timingsByCity?city={}&country={}&method=2".format(city, country)
#     session = aiohttp.ClientSession()
#     while True:
#         try:
#             async with session.get(url) as r:
#                 if r.status == 200:
#                     js = await r.json()
#                     await ctx.send(format_athan(js, city, country))
#         except aiohttp.ServerDisconnectedError as e:
#             print(e)
#             continue
#         except aiohttp.ClientOSError as e:
#             print(e)
#             continue
#         break
#     await session.close()