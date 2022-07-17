from discord.ext import commands
from util import neopixels
import asyncio

class Neopixels(commands.Cog):


    """Lighting control commands."""
    def __init__(self, bot):
        self.bot = bot
        self.is_looping = False
        self.loop_task = None


    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send("Pong!")

    @commands.command()
    async def static(self, ctx, r = 255, g = 255, b = 255):
        self.cancel_loop()

        neopixels.static([r, g, b])
        await ctx.send("Static color set.")

    @commands.command()
    async def wave(self, ctx, wait = 100):
        self.is_looping = True
        self.loop_task = asyncio.ensure_future(neopixels.rainbow_wave(wait / 1000))

        await ctx.send("Rainbow wave set.")

    def cancel_loop(self):
        if self.is_looping:
            self.loop_task.cancel()
            self.is_looping = False

    

def setup(bot):
    bot.add_cog(Neopixels(bot))