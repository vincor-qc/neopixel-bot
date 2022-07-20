from discord.ext import commands
from util import neopixels
import asyncio

# Dict of colors and their rgb values
colors = {
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'orange': (255, 100, 0),
    'purple': (255, 0, 255),
    'cyan': (0, 255, 255),
    'white': (255, 255, 255),
}

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
    async def static(self, ctx, color):
        self.cancel_loop()

        if color in colors:
            color = colors[color]
        else:
            color = self.hex_to_rgb(color)

        neopixels.static(color)
        await ctx.send("Static color set.")

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

        
    # String to RGB color converter
    def hex_to_rgb(self, hex):
        hex = hex.lstrip('#')
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        

    

def setup(bot):
    bot.add_cog(Neopixels(bot))