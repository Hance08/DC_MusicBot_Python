import discord #匯入模組
import asyncio #匯入模組
import os #匯入模組
from discord.ext import commands #匯入模組

intents = discord.Intents.all()
bot = commands.Bot(command_prefix= '/' , intents= intents) # 創建一個 Bot 實例，使用 '/' 作為指令前綴，並啟用所有意圖（Intents）

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f'Now user --> {bot.user} !')
    print(f'{len(slash)} slash commands can be used !')

async def load_extensions():
    for filename in os.listdir("./cogs"):  # 遍歷 "./cogs" 目錄下的所有檔案
        if filename.endswith(".py"): # 如果檔案結尾是 ".py"
            await bot.load_extension(f"cogs.{filename[:-3]}") # 載入該擴展（extension）              


async def main():
    async with bot:  # 使用 Bot 實例建立異步上下文
        await load_extensions() # 載入擴展（extension）
        await bot.start('MTExMjU0MTg5MDU1OTA5ODk3MA.Gt8LpT.dawktOaj2BmeTI88o-olDHnKWS0RT4i70Rb6RY') # 開始 Bot 的運行

asyncio.run(main()) # 執行 main 函式的異步運行