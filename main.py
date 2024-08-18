import os
import discord
import re
from dotenv import load_dotenv
from discord.ext import commands
from src.bright_network_scraper import BrightNetworkScraper
from src.notion_integration import Integration

def parse_embed(embed):
    if embed:
        description = embed.description
        if description:
            url_match = re.search(r'\[Apply here\]\((https?://[^\)]+)\)', description)
            if url_match:
                url = url_match.group(1)
    return url


def main():
    bright_network_scraper = BrightNetworkScraper()
    data = bright_network_scraper.scrape_jobs_page("https://www.brightnetwork.co.uk/internships/technology/")

    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    INTEGRATION_TOKEN = os.getenv('INTEGRATION_TOKEN')
    DATABASE_ID = os.getenv('DATABASE_ID')
    
    notion_integration = Integration(INTEGRATION_TOKEN, DATABASE_ID)

    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True

    # Create an instance of the bot
    intern_scout = commands.Bot(command_prefix='!', intents=intents)

    # Event: Bot is ready
    @intern_scout.event
    async def on_ready():
        print(f'Bot is ready. Logged in as {intern_scout.user}')

    # Command: Display jobs
    @intern_scout.command(name='internships')
    async def display_jobs(ctx):
        for posting in data: 
            embed = discord.Embed(
                title=posting,
                description=f'[Apply here]({data[posting]})',
                color=discord.Color.blue()
            )
            message = await ctx.send(embed=embed)

            # Add reaction to the message
            await message.add_reaction('✅')
    
    @intern_scout.event
    async def on_reaction_add(reaction, user):
        if user.bot:
            return
        if reaction.emoji == '✅':
            message = reaction.message
            embed = message.embeds[0] if message.embeds else None
            url = parse_embed(embed)
            notion_integration._update_notion_page(message.embeds[0].title, url, "Done")

            await message.channel.send(f"Saved {message.embeds[0].title} to Notion page.")

    # Run the bot
    intern_scout.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()