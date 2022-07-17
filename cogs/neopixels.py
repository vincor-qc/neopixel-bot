from discord.ext import commands
from util import neopixels

class Neopixels(commands.Cog):
    """Lighting control commands."""
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send("Pong!")

    @commands.command()
    async def static(self, ctx, r = 255, g = 255, b = 255):
        neopixels.static([r, g, b])

        await ctx.send("Static color set.")

def setup(bot):
    bot.add_cog(Neopixels(bot))