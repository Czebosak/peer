import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.commands import Option
from .. import config

class events(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(guild_ids=[972791561450573824], name="clear", description="description clear")
    @discord.default_permissions(manage_messages=True)
    async def clear(self, ctx, amount:
        Option(
            int,
            "The amount of messages you want to clear",
            required=True
        )
    ):
        if amount > 100:
            amount = 100
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f"Successfuly cleared {amount} message(s).")


    @commands.slash_command(guild_ids=[972791561450573824], name="warn", description="Warn a user")
    @discord.default_permissions(kick_members=True)
    async def warn(self, ctx, user:
        Option(
            discord.Member,
            "The user that you want to warn",
            required=True
        ),
        reason:
        Option(
            str,
            "reason",
            required=False,
            default=None
        ),
    ):
        if ctx.author == user:
            ctx.respond("You cannot warn yourself!")
            return
        
        async def interaction_a(interaction):
            result = await config.stat(user=user, stat="warnings", to=reason)

            if not interaction.user == ctx.author:
                return
            elif result is False:
                await ctx.send("The user has 15 warnings!")
            else: 
                await interaction.message.delete()
                await ctx.send(f"You warned {user.mention} for {reason}!")
                await user.send(f"You have been warned for `{reason}` in the server `{ctx.channel.guild}`!") 


        async def interaction_b(interaction):
            if not interaction.user == ctx.author:
                return
            await interaction.message.delete()
            await ctx.send("Action canceled!")

        button = Button(emoji=config.emojis["checkmark"], style=discord.ButtonStyle.success)
        button2 = Button(emoji=config.emojis["x"], style=discord.ButtonStyle.danger)

        button.callback = interaction_a
        button2.callback = interaction_b
        view = View(button, button2)

        embed = discord.Embed(title="Hold up!", description=f"Are you sure you want to warn {user.mention}?")
        embed.add_field(name="Reason:", value=reason, inline=False)

        await ctx.respond(embed=embed, view=view)


    @commands.slash_command(guild_ids=[972791561450573824], name="warnings", description="Warn a user")
    @discord.default_permissions(kick_members=True)
    async def warnings(self, ctx, user:
        Option(
            discord.Member,
            "The user that you want to warn",
            required=True
        )
    ):
        warnings = await config.stat(user=str(user.id), stat="warnings", action="get")

        content = ""

        for i in warnings:
            content += i + "\n"
        
        embed = discord.Embed(title=f"List of warnings of {user.name}", description=content, color=config.c_main)
        await ctx.respond(embed=embed)

    # TODO Move moderaton commands to this cog

def setup(client):
    client.add_cog(events(client))
