from discord.ext import commands as cum
from discord.utils import get
import discord
import random
from discord.ui import Button, View
import sqlite3
import config
import validators

prefix = config.PREFIX


class ForAll(cum.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cum.command()
    async def random(self, ctx, number1=1, number2=10):
        a = random.randint(number1, number2)
        await ctx.send(f"Ваше число: {a}")

    @cum.command(pass_context=True)
    async def randomp(self, ctx):
        db = sqlite3.connect("eco.sqlite")
        cursor = db.cursor()

        cursor.execute("SELECT url FROM aaa")
        results = cursor.fetchall()
        if results:
            url = random.choice(results)[0]
            emb = discord.Embed(title="Случайная фотография",
                                color=discord.Colour.gold())
            emb.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar)
            emb.set_footer(
                text=f"Вы можете добавить собственную фотографию, написав {config.PREFIX}sendp и указав на нее ссылку",
                icon_url=ctx.author.avatar)
            emb.set_image(url=url)
            await ctx.send(embed=emb)
        else:
            await ctx.send("Список ссылок пуст")

    @cum.command()
    async def sendp(self, ctx, url1):
        print(validators.url(url1))
        if validators.url(url1):
            db = sqlite3.connect("eco.sqlite")
            cursor = db.cursor()
            sql = "INSERT INTO aaa (url) VALUES (?)"
            cursor.execute(sql, (url1,))
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("Отправлено")
        else:
            await ctx.send("Вы отправили не ссылку")

    @cum.command()
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            await ctx.send("я присоединился к каналу")

    @cum.command()
    async def leave(self, ctx):
        global voice
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()
        await ctx.send("я отключился от канала")

    @cum.command()
    async def profile(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        db = sqlite3.connect("eco.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT wallet, rep, lvl FROM eco WHERE user_id = {member.id}")
        balance = cursor.fetchone()
        try:
            wallet = balance[0]
            rep = balance[1]
            lvl = balance[2]
        except:
            wallet = 0
            lvl = 1
            rep = 0
        emb = discord.Embed(title="Ваш профиль", color=discord.Colour.dark_gray())
        emb.add_field(name=f"Ваш уровень:",
                      value=lvl,
                      inline=True)
        emb.add_field(name=f"Ваш баланс:",
                      value=wallet,
                      inline=True)
        emb.add_field(name=f"Ваша репутация:",
                      value=rep,
                      inline=True)
        await ctx.send(embed=emb)

    @cum.command()
    async def help(self, ctx):
        emb = discord.Embed(title="Команды для администрации",
                            color=discord.Colour.dark_gray())
        emb.add_field(name="{}clear".format(prefix),
                      value='Очистить сообщения в чате (число)',
                      inline=True)
        emb.add_field(name="{}kick".format(prefix),
                      value='Выгнать кого-то с сервера',
                      inline=False)
        emb.add_field(
            name="{}ban".format(prefix),
            value='Забанить человека на сервере (используйте в крайних случаях)',
            inline=False)

        emb2 = discord.Embed(title='Команды для всех',
                             color=discord.Colour.dark_gray())
        emb2.add_field(name=f"{prefix}profile",
                       value='Можно посмотреть ваш профиль на сервере',
                       inline=False)
        emb2.add_field(name=f"{prefix}join",
                       value='Зайти в голосовой канал',
                       inline=False)
        emb2.add_field(name=f"{prefix}leave", value='Выйти из голосового канала')
        emb2.add_field(name=f"{prefix}random (number1, number2)",
                       value='Случайное число в диапазоне',
                       inline=False)
        emb2.add_field(name=f"{prefix}randomp",
                       value='Случайная фотография',
                       inline=False)

        async def right(interaction: discord.Interaction):
            await message.edit(embed=emb2)
            await interaction.response.defer()

        async def left(interaction: discord.Interaction):
            await message.edit(embed=emb)
            await interaction.response.defer()

        button_left = Button(label="<", style=discord.ButtonStyle.success)
        button_right = Button(label=">", style=discord.ButtonStyle.success)

        button_right.callback = lambda interaction: right(interaction)
        button_left.callback = lambda interaction: left(interaction)
        view = View()
        message = await ctx.send(embed=emb)
        view.add_item(button_left)
        view.add_item(button_right)
        await ctx.send(view=view)


async def setup(bot):
    await bot.add_cog(ForAll(bot))
