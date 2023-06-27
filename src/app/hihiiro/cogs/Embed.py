import discord
from discord.ext import commands
from hihiiro.core.bot import DBot

class Embed(commands.Cog):
    def __init__(self, bot: DBot):
        self.bot = bot

    @commands.command()
    async def embed(self, ctx: commands.Context):
        embed = discord.Embed()
        embed.color = 0xff0000
        embed.title = '埋め込み要素'
        embed.description = 'ここに説明'
        embed.set_author(name='書いた人',url='https://google.com')
        embed.set_thumbnail(
            url='https://cdn.pixabay.com/photo/2020/08/10/14/17/hummingbird-5477966_960_720.jpg'
        )
        embed.set_image(
            url='https://cdn.pixabay.com/photo/2020/08/07/09/23/flower-5470156_960_720.jpg'
        )
        embed.add_field(name='犬', value='従順')
        embed.add_field(name='猫', value='気まま')
        embed.add_field(name='牛', value='おいしい')
        embed.add_field(name='馬', value='とてもおいしい')
        embed.add_field(name='羊', value='すごくおいしい')
        embed.add_field(name='🍣', value='おいしい！')
        embed.add_field(name='インライン表示', value='無効にする', inline=False)
        embed.add_field(name='value部分は',
                        value='`Markdown`が**使える**', inline=False)
        embed.set_footer(text="フッターテキスト")
        await ctx.send("Embedの例", embed=embed)


async def setup(bot):
    await bot.add_cog(Embed(bot))