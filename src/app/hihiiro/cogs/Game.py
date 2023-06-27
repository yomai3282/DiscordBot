import discord,random
from discord.ext import commands
from discord.ext.commands.errors import (
    BadArgument,
    TooManyArguments,
    MissingRequiredArgument,
    MissingPermissions,
    CommandOnCooldown
)
from hihiiro.core.bot import DBot

class Game(commands.Cog):
    def __init__(self, bot: DBot):
        self.bot = bot
    
    @commands.command(ignore_extra=False)
    @commands.cooldown(rate=2, per=60, type=commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def dice(self, ctx: commands.Context, a: int, b: int):
        result = random.choices(range(1, b + 1), k=a)
        return await ctx.send(
            f'{a}D{b}の結果は{sum(result)}です．\n内訳{result}'
        )
    @dice.error
    async def on_dice_error(self, ctx: commands.Context, error):
        if isinstance(error, BadArgument):
            return await ctx.send('引数はいずれも整数です')
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send('引数は2つ必要です')
        if isinstance(error, TooManyArguments):
            return await ctx.send('必要な引数は2つのみです')
        if isinstance(error, MissingPermissions):
            return await ctx.send('管理者のみが実行可能です')
        if isinstance(error, CommandOnCooldown):
            return await ctx.send('1分間に2回まで実行可能です')
    
    @commands.Cog.listener(name='on_message')
    async def on_ready(self,message):
        if message.author.bot:
            return
        if 'いいね' in message.content:
            await message.add_reaction('\U0001f44d')
            
    @commands.command()
    async def test(self,ctx):
        await ctx.send("test")

async def setup(bot):
    await bot.add_cog(Game(bot))