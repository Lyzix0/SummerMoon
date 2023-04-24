from discord.ext import commands as cum
import sqlite3


class Events(cum.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cum.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("eco.sqlite")
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS eco ( 
        user_id INT, 
        wallet INT, 
        rep INT,
        lvl INT
    )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS aaa (url TEXT)''')
        print("I am ready!")

    @cum.Cog.listener()
    async def on_typing(self, channel, user, when):
        print(f'{user} печатал в {channel} в {str(when)[11:-6]}')

    @cum.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
        print(str(ctx.author) + ": " + str(ctx.content))
        author = ctx.author
        db = sqlite3.connect("eco.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM eco WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = "INSERT INTO eco (user_id, wallet, rep, lvl) VALUES (?, ?, ?, ?)"
            val = (author.id, 100, 0, 1)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @cum.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            print("yes")
            to_send = f'Добро пожаловать {member.mention} на сервер {guild.name}!'
            await guild.system_channel.send(to_send)


async def setup(bot):
    await bot.add_cog(Events(bot))
