from discord.ext import commands as cum
from discord.utils import get
from discord.ui import Button, View
import discord
import random
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
    async def randomphoto(self, ctx):
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
    async def sendphoto(self, ctx, url1):
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
        emb = discord.Embed(title=f"Профиль {member.display_name}", color=discord.Colour.dark_gray())
        emb.add_field(name=f"Уровень:",
                      value=lvl,
                      inline=True)
        emb.add_field(name=f"Баланс:",
                      value=f"{wallet} 🦜",
                      inline=True)
        emb.add_field(name=f"Репутация:",
                      value=rep,
                      inline=True)
        await ctx.send(embed=emb)

    @cum.command()
    async def sendmoney(self, ctx, member: discord.Member = None, money: int = None):
        if member != None:
            if money is not None:
                if money > 0:
                    db = sqlite3.connect("eco.sqlite")
                    cursor = db.cursor()
                    cursor.execute(f"UPDATE eco SET wallet = wallet + {money} WHERE user_id = {member.id}")
                    cursor.execute(f"UPDATE eco SET wallet = wallet - {money} WHERE user_id = {ctx.author.id}")
                    db.commit()
                    await ctx.send("Отправлено!")
                else:
                    await ctx.send("Укажите количество 🦜 больше нуля")
            else:
                await ctx.send("Укажите количество 🦜")
        else:
            await ctx.send("Укажите того, кому хотите отправить 🦜")

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
        emb2.add_field(name=f"{prefix}randomphoto",
                       value='Случайная фотография',
                       inline=False)

        emb3 = discord.Embed(title="Экономика",
                             color=discord.Colour.dark_gray())
        emb3.add_field(name=f"{prefix}sendmoney (кому, кол-во)",
                       value='Отправить пользователю  🦜',
                       inline=False)

        async def first(interaction: discord.Interaction):
            await message.edit(embed=emb)
            await interaction.response.defer()

        async def second(interaction: discord.Interaction):
            await message.edit(embed=emb2)
            await interaction.response.defer()

        async def third(interaction: discord.Interaction):
            await message.edit(embed=emb3)
            await interaction.response.defer()

        button_one = Button(label="1", style=discord.ButtonStyle.success)
        button_two = Button(label="2", style=discord.ButtonStyle.success)
        button_three = Button(label="3", style=discord.ButtonStyle.success)

        button_one.callback = lambda interaction: first(interaction)
        button_two.callback = lambda interaction: second(interaction)
        button_three.callback = lambda interaction: third(interaction)
        view = View()
        message = await ctx.send(embed=emb)
        view.add_item(button_one)
        view.add_item(button_two)
        view.add_item(button_three)
        await ctx.send(view=view)

    # @cum.command()
    # async def work(self, ctx):
    #     print("worked")
    #     last_work_time = await self.bot.redis.get(f"last_work_time:{ctx.author.id}")
    #
    #     if last_work_time is not None and (time := time.time() - float(last_work_time)) < 4 * 60 * 60:
    #         remaining_time = int(4 * 60 * 60 - time)
    #         await ctx.send(
    #             f"You can use this command again in {remaining_time // 3600} hours, {(remaining_time % 3600) // 60} minutes, and {remaining_time % 60} seconds.")
    #     else:
    #         await self.bot.redis.set(f"last_work_time:{ctx.author.id}", str(time.time()))
    #         await ctx.send("You have earned 100 currency units for your work!")


async def setup(bot):
    await bot.add_cog(ForAll(bot))
