from curses.ascii import isdigit
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
        self.speed = 1


    # Pong!
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    # Sets a speed
    @commands.command()
    async def speed(self, ctx, speed):
        if isdigit(speed):
            neopixels.set_wait(0.01 / int(speed))
            await ctx.send("Speed set to {}x".format(speed))
        else:
            await ctx.send("Invalid speed")

    # Sets a brightness between 0 and 1
    @commands.command()
    async def brightness(self, ctx, brightness):
        try:
            brightness = float(brightness)
            if brightness < 0 or brightness > 1:
                await ctx.send("Invalid brightness")
            else:
                neopixels.set_brightness(brightness)
                await ctx.send("Brightness set to {}".format(brightness))
        except ValueError:
            await ctx.send("Invalid brightness")
       

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

    # Sets a gradient color
    @commands.command()
    async def gradient(self, ctx, *args):
        self.cancel_loop()

        cargs = []
        for arg in args:
            if arg in colors:
                cargs.append(colors[arg])
            else:
                cargs.append(self.hex_to_rgb(arg))

        self.is_looping = True
        self.loop_task = asyncio.ensure_future(neopixels.gradient(cargs))
        await ctx.send("Gradient color set.")

    # Starts a rainbow wave (all pixels are different colors)
    @commands.command()
    async def wave(self, ctx):
        self.cancel_loop()
        self.is_looping = True
        self.loop_task = asyncio.ensure_future(neopixels.rainbow_wave())

        await ctx.send("Rainbow wave set.")

    # Starts a rainbow cycle (all pixels the same color)
    @commands.command()
    async def cycle(self, ctx):
        self.cancel_loop()

        self.is_looping = True
        self.loop_task = asyncio.ensure_future(neopixels.rainbow_cycle())

        await ctx.send("Rainbow cycle set.")

    # Starts a rainbow breathing pattern
    @commands.command()
    async def rbreathe(self, ctx):
        self.cancel_loop()

        self.is_looping = True
        self.loop_task = asyncio.ensure_future(neopixels.rainbow_breathing())

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

    # Cancel Looping Tasks
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
