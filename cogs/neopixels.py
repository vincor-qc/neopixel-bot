from discord.ext import commands
from util import neopixels
import asyncio

class Neopixels(commands.Cog):


    """Lighting control commands."""
    def __init__(self, bot):
        self.bot = bot
        self.is_looping = False
        self.loop_task = None


    # Pong!
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    # Sets a static color
    @commands.command()
    async def static(self, ctx, r = 255, g = 255, b = 255):
        self.cancel_loop()

        neopixels.static([r, g, b])
        await ctx.send("Static color set.")
    
    # Sets starry night mode
    @commands.command()
    async def starry_night(self, ctx, r, g, b, wait = 100):
        self.cancel_loop()

        self.loop_task = asyncio.ensure_future(neopixels.starry_night([r, g, b], wait))
        self.is_looping = True
        await ctx.send("Starry Night mode set.")

    # Sets the periodic mode
    @commands.command()
    async def periodic(self, ctx, r, g, b, wait = 100):
        self.cancel_loop()

        self.loop_task = asyncio.ensure_future(neopixels.periodic([r, g, b], wait))
        self.is_looping = True
        await ctx.send("Periodic mode set.")

    # Starts a rainbow wave (all pixels are different colors)
    @commands.command()
    async def wave(self, ctx, wait = 100):
        self.cancel_loop()

        self.is_looping = True
        self.loop_task = asyncio.ensure_future(neopixels.rainbow_wave(wait / 100000))

        await ctx.send("Rainbow wave set.")

    # Starts a rainbow cycle (all pixels the same color)
    @commands.command()
    async def cycle(self, ctx, wait = 100):
        self.cancel_loop()

        self.is_looping = True
        self.loop_task = asyncio.ensure_future(neopixels.rainbow_cycle(wait / 100000))

        await ctx.send("Rainbow cycle set.")

    # Starts a rainbow breathing pattern
    @commands.command()
    async def rbreathe(self, ctx, wait = 10):
        self.cancel_loop()

        self.is_looping = True
        self.loop_task = asyncio.ensure_future(neopixels.rainbow_breathing(wait / 100000))

        await ctx.send("Rainbow breathing set.")

    # Sets a random color
    @commands.command()
    async def random(self, ctx):
        self.cancel_loop()

        neopixels.random_color()
        await ctx.send("Random color set.")

    # Clears the pixels
    @commands.command()
    async def clear(self, ctx):
        self.cancel_loop()

        neopixels.clear()
        await ctx.send("Lighting cleared.")

    def cancel_loop(self):
        if self.is_looping:
            self.loop_task.cancel()
            self.is_looping = False
        

    

def setup(bot):
    bot.add_cog(Neopixels(bot))