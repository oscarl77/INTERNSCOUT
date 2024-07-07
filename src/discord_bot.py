import discord
from discord.ext import commands

class DiscordBot(commands.Bot):

    def __init__(self, data, command_prefix='!', token=None, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=command_prefix, intents=intents, **kwargs)
        self.token = token
        self.data = data
        self.add_command(self.jobs_command)

    async def on_ready(self):
        print(f'InternScout is ready. Logged in as {self.user}')
    
    @commands.command(name='jobs')
    async def jobs_command(self, ctx):
        response = ""
        for posting in self.data:
            response += f"INTERNSHIP: {posting}\n"
        await ctx.send(response)
    
    def run(self):
        super().run(self.token)