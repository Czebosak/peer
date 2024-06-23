import discord
from discord.ext import commands
# from antispam import AntiSpamHandler
# from antispam.enums import Library
from .. import config
import json

bad_words = (
    "fuck",
    "dick",
    "nigga",
    "bitch",
    "rape",
    "stfu"
)

bypass = {
    "0": "o",
    "1": "i",
    "3": "e",
    "4": "a",
    "$": "s"
}

prefix = "$p "

class event(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @commands.Cog.listener()
    async def on_guild_join(guild):
        with open("app/data/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "$p "

        with open("app/data/prefixes.json", "w") as f:
            json.dump(prefixes, f)


    @commands.Cog.listener()
    async def on_guild_remove(guild):
        with open("app/data/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open("app/data/prefixes.json", "w") as f:
            json.dump(prefixes, f)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.client.get_channel()
        await channel.send(f'Hi {member.mention}! Welcome to the server!')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if len(message.content) < 428:
                if "https://" in message.content.lower() or "http://" in message.content.lower():
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Don't send links!")
                elif message.content.lower() in bad_words:
                    await message.delete()
                    await message.channel.send(f"{message.author.mention} Don't swear!")
                elif self.client.user.mentioned_in(message):
                    await message.channel.send("Hi!")
                else:
                    await config.stat(user=message.author, stat="messages_sent", to=1, guild=message.guild)
                    levelup = await config.add_xp(user=message.author, xp=1)
                    if levelup is True:
                        editor = await config.generate_rank_card(message.author)
                        editor.save("rank_card.png")
                        await message.channel.send("Level up!", file=discord.File("rank_card.png"))
                    await self.client.process_commands(message)
            else:
                await message.delete()
                await message.channel.send(f"{message.author.mention} Don't post blocks of text!")
    
    
    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if threadage.content.lower() in bad_words:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Don't swear!")


def setup(client):
    client.add_cog(event(client))
