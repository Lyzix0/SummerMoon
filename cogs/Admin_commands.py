from discord.ext import commands as cum
import discord


class Admin(cum.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cum.command()
    @cum.has_permissions(manage_messages=True)
    async def clear(self, ctx, arg=2):
        if arg > 10:
            arg = 10
        await ctx.channel.purge(limit=arg)

    @cum.command()
    @cum.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        user = await self.bot.fetch_user(member.id)
        await user.send(f'Тебя выгнали с сервера. Причина: {reason}')
        await ctx.send(f"Участник {member.mention} выгнан с сервера")

    @cum.command()
    @cum.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"Участник {member.mention} был зверзко забанен")


async def setup(bot):
    await bot.add_cog(Admin(bot))