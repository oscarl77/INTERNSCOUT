import os
import discord
from discord.ext import commands
from src.discord_bot import DiscordBot
from src.bright_network_scraper import BrightNetworkScraper

def main():
    bright_network_scraper = BrightNetworkScraper()
    data = bright_network_scraper.scrape_jobs_page("https://www.brightnetwork.co.uk/internships/")
    token = os.getenv('DISCORD_TOKEN')
    better_token = 'MTI1OTI3MTM5NDQ5MTg5NTg1OQ.GLll2q.aYoCsaEWVUGcdoSf1143AruSR8gSwf5uoxK-w4'

    # Intents (required for bots with newer Discord API)
    intents = discord.Intents.default()
    intents.message_content = True

    # Create an instance of the bot
    intern_scout = commands.Bot(command_prefix='!', intents=intents)

    # Event: Bot is ready
    @intern_scout.event
    async def on_ready():
        print(f'Bot is ready. Logged in as {intern_scout.user}')

    # Command: Display jobs
    @intern_scout.command(name='jobs')
    async def display_jobs(ctx):
        for posting in data:
            embed = discord.Embed(
                title=posting,
                description=f'[Apply here]({data[posting]})',
                color=discord.Color.blue()
            )
            print(data[posting])
            await ctx.send(embed=embed)
            break

    # Run the bot
    intern_scout.run(better_token)

if __name__ == "__main__":
    main()