import discord
from discord.ext import commands
from discord.commands import Option
from easy_pil import Canvas, Editor
from io import BytesIO

class fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=[972791561450573824], name="wanted", description="Work")
    async def wanted(self, ctx):
        canvas = Canvas((525, 763), color="black")
        bg = Editor(image="app/assets/img/wanted.png")
        pfp = Editor(image=BytesIO(await ctx.author.display_avatar.read())).resize((250, 250))

        editor = Editor(canvas)
        editor.paste(image=bg.image, position=(0, 0))
        editor.paste(image=pfp.image, position=(262 - 125, 382 - 125))
        editor.save("wanted.png")

        await ctx.respond(file=discord.File("wanted.png"))


def setup(client):
    client.add_cog(fun(client))
