import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.commands import Option
from .. import config
from ..config.responses import get_response
from ..config.items import *
from ..config.job import *
from datetime import datetime
import random

class economy(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.slash_command(guild_ids=[972791561450573824], name="shop", description="Shows the shop")
    async def shop(self, ctx):
        embed = discord.Embed(title=f"Shop", description="", color=config.c_main)

        for i in items:
            if i["buyable"] is True:
                embed.add_field(name=f'\n{i["icon"]} {i["name"]}', value=f'> *{config.format_number(i["price"][0])}🍌*\n> {i["description"]}', inline=False)
        
        await ctx.respond(embed=embed)

    
    @commands.slash_command(guild_ids=[972791561450573824], name="buy", description="Buy an item from the shop")
    async def buy(self, ctx, item:
        Option(
            str,
            "The user that you want to warn",
            required=True
        )
    ):
        await config.open_account(ctx.author)
        
        money = await config.get_specific_bank_data(ctx.author)

        item_data = await get_item(item)
        
        if item_data == False:
            await ctx.respond("Could not find that item!")

        if item_data["price"][0] <= money[0]:
            await config.update_bank_data(user=ctx.author, change=item_data["price"][0] * -1)

            await add_item(item=item_data["uuid"], id=ctx.author.id)

            await ctx.respond(f'Successfully bought **{item_data["icon"]} {item_data["name"]}**')
        else:
            await ctx.respond("You cannot afford this!")
    

    @commands.slash_command(guild_ids=[972791561450573824], name="sell", description="Sell an item from your inventory")
    async def sell(self, ctx, item:
        Option(
            str,
            "The user that you want to warn",
            required=True
        )
    ):
        await config.open_account(ctx.author)

        item_data = await get_item(item_id=item)

        item_check = await get_item(item_id=item_data["uuid"], inventory="player_inventories", by="uuid", id=ctx.author.id)

        if item_check is False:
            await ctx.respond("You don't have that item!")
        else:
            if item_data["sellable"] is True:
                await config.update_bank_data(user=ctx.author, change=random.rndint(round(item_data["price"][0] * 0.8, round(item_data["price"][1]) * 0.8)))

                await remove_item(item=item_data, id=ctx.author.id)

                await ctx.respond(f'Successfully sold **{item_data["icon"]} {item_data["name"]}** for {config.format_number(round(item_data["price"][0] * 0.8))}')
            else:
                await ctx.respond("You cannot sell this item!")
        
    
    @commands.slash_command(guild_ids=[972791561450573824], name="inventory", description="Shows your inventory")
    async def inventory(self, ctx, user:
        Option(
            discord.Member,
            "The user that you want to warn",
            required=False,
            default=None
        )
    ):
        if user is None:
            user = ctx.author

        item_uuids = await get_inventory(id=user.id)

        item_data = []

        for i in item_uuids:
            item_data.append(await get_item(item_id=i, by="uuid"))

        embed = discord.Embed(title=f"{user.display_name}'s Inventory", description="Looks like your inventory is empty!", color=config.c_main)

        for i in item_data:
            if i["buyable"] is True and i["sellable"] is True:
                embed.add_field(name=f'\n{i["icon"]} {i["name"]}', value=f'> \n> Selling in the store for: {config.format_number(i["price"][0])} Selling for: {config.format_number(round(i["price"][0] * 0.8))}/{round(i["price"][1] * 0.8)}🍌{i["description"]}', inline=False)
            elif i["buyable"] is False and i["sellable"] is True:
                embed.add_field(name=f'\n{i["icon"]} {i["name"]}', value=f'> Selling for: {config.format_number(round(i["price"][0] * 0.8))}/{config.format_number(round(i["price"][1] * 0.8))}🍌\n> {i["description"]}', inline=False)
            elif i["buyable"] is True and i["sellable"] is False:
                embed.add_field(name=f'\n{i["icon"]} {i["name"]}', value=f'> Selling in the store for: {config.format_number(i["price"][0])}🍌\n> {i["description"]}', inline=False)
            else:
                embed.add_field(name=f'\n{i["icon"]} {i["name"]}', value=f'> *Not for sale*\n> {i["description"]}', inline=False)

            embed.description = ""
        
        await ctx.respond(embed=embed)
    

    @commands.slash_command(guild_ids=[972791561450573824], name="rank", description="Shows your rank card")
    async def rank(self, ctx):
        await self.client.fetch_user(ctx.author.id)

        # usercolor = await config.convert_to_rgb(ctx.author.accent_color)  

        editor = await config.generate_rank_card(ctx.author)
        editor.save("rank_card.png")

        await ctx.respond(file=discord.File("rank_card.png"))

    
    @commands.slash_command(guild_ids=[972791561450573824], name="work", description="Work")
    async def work(self, ctx):
        await config.open_account(ctx.author)
        data = await config.get_specific_user_skills(user=ctx.author, type="work")
        
        if not data == "none":
            for key, value in jobs.items():
                if key == data[1]:
                    job = value
        
        if not data[2] == "none":
            duration = config.duration(datetime.now, data[2])

            if not duration >= 3600:
                await ctx.respond(f"You need to wait {round(duration * 60, 1)} minutes to use this command!")
                return
        
        paycheck = random.randint(job["money"][0], job["money"][1])
        work_xp = 12

        await config.update_bank_data(user=ctx.author, change=paycheck)

        await ctx.respond(f"You have earned {paycheck}🍌 and {work_xp} work XP!")


def setup(client):
    client.add_cog(economy(client))
