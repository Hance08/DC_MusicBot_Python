import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= '/' , intents= intents)

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f'Now user --> {bot.user} !')
    print(f'{len(slash)} can be used !')
    
async def main():
    async with bot:
        await bot.start('MTExMjU0MTg5MDU1OTA5ODk3MA.Gt8LpT.dawktOaj2BmeTI88o-olDHnKWS0RT4i70Rb6RY')