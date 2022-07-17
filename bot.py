import os
import sys

import discord
import dotenv
from discord.ext import commands

# Load variables from the .env file.
dotenv.load_dotenv()

# Allowed servers
allowed_servers = [645753006352236544]

# Create a new bot instance with the prefix "!"
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
	print(f"successfully logged in as {bot.user}")

@bot.event
async def on_message(msg):

    # If the message is from a server that we want to allow, then process it.
    if msg.guild.id in allowed_servers:
        await bot.process_commands(msg)
    else:
        await msg.channel.send("This bot is not allowed to run in this server.")

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, (commands.CommandOnCooldown, commands.UserInputError)):
		await ctx.send(str(error))

# Loads all extensions in the cogs folder.
initial_exts = ["cogs.neopixels"]

def main():
	token = os.getenv("DISCORD_TOKEN")
	if not token:
		print("no token specified; make sure you have a .env file with a DISCORD_TOKEN entry")
		sys.exit(1)
	
	for ext in initial_exts:
		bot.load_extension(ext)
	bot.run(token)

if __name__ == "__main__":
	main()