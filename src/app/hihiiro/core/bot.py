from discord.ext import commands
import asyncio

class DBot(commands.Bot):
    def __init__(self, INTENTS):
        super().__init__(
            command_prefix="!",
            intents=INTENTS
            )
        asyncio.run(self.load_cogs())

    async def load_cogs(self):
        cogs = ["hihiiro.cogs.Game","hihiiro.cogs.Embed"]
        for cog in cogs:
            await self.load_extension(cog)
            print(cog + "をロードしました")

    async def on_ready(self):
        print('起動しました')

