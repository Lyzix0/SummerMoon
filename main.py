import os
import discord
from discord.ext import commands
import asyncio
import config

intents = discord.Intents.all()
prefix = config.PREFIX
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"cogs.{filename[:-3]}")


@bot.command()
async def reload(ctx):
    print(ctx.author.id)
    if ctx.author.id == 710403299245031585:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.unload_extension(f"cogs.{filename[:-3]}")
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
        await ctx.send("Обновлено")
    else:
        await ctx.send('Вы не являетeсь разработчиком бота')


async def main():
    async with bot:
        await load()
        await bot.start(config.TOKEN)


asyncio.run(main())
