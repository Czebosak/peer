import discord
import random
import asyncio
from discord.ext import commands
from discord.ui import Button, Select, View
from discord.commands import Option
import requests
import datetime
import app.config
from os import listdir
from json import load, dump
from app.config.responses import get_response

intents = discord.Intents().all()

def get_prefix(client, message):
    with open("app/data/prefixes.json") as f:
        prefixes = load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix, intents=intents)

# Load cogs from cogs folder
if __name__ == "__main__":
    for filename in listdir("./app/cogs"):
        if filename.endswith(".py"):
            client.load_extension("app.cogs." + filename[:-3])


@client.event
async def on_ready():
    print("Bot started {0.user}".format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for $p"))


#@client.event
#async def on_command_error(ctx, error):
#    title = "❌ An error occurred!"
#
#    if isinstance(error, commands.MissingRequiredArgument):
#        message = "Missing required arguments"
#    elif isinstance(error, commands.MissingPermissions):
#        message = "Missing permissions"
#    elif isinstance(error, commands.CommandOnCooldown):
#        title = get_response(type="cooldown")
#        message = "This command is on cooldown. Try again in {:.2f} seconds".format(error.retry_after)
#    elif isinstance(error, commands.CommandNotFound):
#        message = "Unknown command"
#    else:
#        message = "An unknown error occurred"
#    embed = discord.Embed(title=title, description=message, color=0xdd2e44)
#    await ctx.send(embed=embed)


@commands.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    if ctx.author == ctx.guild.owner:
        await ctx.send("Alright!\nLet's guide you through the setup.")

        messages = [
            {"message":"Do you want to verify new members?", "setting":"verify", "channel":False, "string":False},
            {"message":"Sweet!\nShould swear words be allowed in your server?", "setting":"safe", "channel":False, "string":False},
            {"message":"Great!\nWhere do you want to send welcome messages (type None to disable this feature)?", "setting":"welcome", "channel":True, "string":True}
        ]

        button = Button(emoji="<:peer_checkmark:978689943410991114>", style=discord.ButtonStyle.success)
        button2 = Button(emoji="<:peer_x:978689943205470288>", style=discord.ButtonStyle.danger)


        view = View(button, button2)

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in messages:
            if i["string"] is False and i["channel"] is False:
                async def interaction_a(interaction):
                    if not interaction.user == ctx.author:
                        return;
                    
                    await app.config.config(id=ctx.author.id, type="guilds", mode="change", setting=i["setting"], value=True)


                async def interaction_b(interaction):
                    if not interaction.user == ctx.author:
                        return;
                    
                    await app.config.config(id=ctx.author.id, type="guilds", mode="change", setting=i["setting"], value=False)
                
                button.callback = interaction_a
                button2.callback = interaction_b

                ctx.send(i["message"], view=view)
            elif i["string"] is True and i["channel"] is True:
                try:
                    ctx.send(i["message"])
                    response = await client.wait_for("message", timeout=15.0, check=check)
                    if response.lower() == "none" or response.lower() == "false" or response.lower() == "no":
                        await app.config.config(id=ctx.author.id, type="guilds", mode="change", setting=i["setting"], value=False)
                    elif response.channel_mention:
                        print("hi")
                    else: await ctx.send("")
                    
                except asyncio.TimeoutError:
                    await ctx.send("You didn't answer the question in time.")
                    return;
    else:
        await ctx.send("You are not the server owner")


@client.command()
async def hello(ctx):
    response = random.randint(0, 2)

    if response == 0:
        await ctx.send("Hi!")
    elif response == 1:
        await ctx.send("Hello")
    else:
        await ctx.send("Yo")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! Executed within {round(client.latency * 1000)}ms")


@client.command()
async def prefix(ctx, *, prefix):
    with open("app/data/prefixes.json", "r") as f:
            prefixes = load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("app/data/prefixes.json", "w") as f:
        dump(prefixes, f)
    
    await ctx.send(f'Successfully changed the prefix to: "{prefix}"')


@client.command()
async def reload(ctx, cog):
    if ctx.author.id == 594096796314238976:
        client.load_extension("app.cogs." + cog)


@client.command(aliases=["rate", "review"])
async def feedback(ctx):
    select = Select(
        placeholder="Rate your experience",
        options=[
            discord.SelectOption(label="Great", emoji="😎"),
            discord.SelectOption(label="Good", emoji="🙂"),
            discord.SelectOption(label="Meh", emoji="😑"),
            discord.SelectOption(label="Poor", emoji="🙁"),
            discord.SelectOption(label="Bad", emoji="😡")
        ])

    async def interaction(interaction):
        await interaction.channel.send("Processing...")
        with open("data/feedback.json", "r") as f:
            users = load(f)

        user = interaction.user.id

        if str(user) in users:
            await interaction.channel.send("Updating your review...")

        users[str(user)] = {}
        users[str(user)]["rating"] = select.values[0]
        users[str(user)]["date"] = datetime.date.today()

        with open("data/feedback.json", "w") as f:
            dump(users, f)

        await interaction.response.send_message("Feedback sent!")

    select.callback = interaction

    view = View(select)

    await ctx.send("Send feedback", view=view)


@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        async def interaction_a(interaction):
            if not interaction.user == ctx.author:
                return
            await interaction.message.delete()
            await member.kick(reason=reason)
            await ctx.send(f"Successfully kicked {member}!")

        async def interaction_b(interaction):
            if not interaction.user == ctx.author:
                return
            await interaction.message.delete()
            await ctx.send("Action canceled!")

        button = Button(emoji="<:peer_checkmark:978689943410991114>", style=discord.ButtonStyle.success)
        button2 = Button(emoji="<:peer_x:978689943205470288>", style=discord.ButtonStyle.danger)

        button.callback = interaction_a
        button2.callback = interaction_b
        view = View(button, button2)

        embed = discord.Embed(title="Hold up!", description=f"Are you sure you want to kick {member.mention}?")
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("Error!")


@client.command()
@commands.has_permissions(kick_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        async def interaction_a(interaction):
            if not interaction.user == ctx.author:
                return
            await interaction.message.delete()
            await member.ban(reason=reason)
            await ctx.send(f"Successfully banned {member}!")

        async def interaction_b(interaction):
            if not interaction.user == ctx.author:
                return
            await interaction.message.delete()
            await ctx.send("Action canceled!")

        button = Button(emoji="<:peer_checkmark:978689943410991114>", style=discord.ButtonStyle.success)
        button2 = Button(emoji="<:peer_x:978689943205470288>", style=discord.ButtonStyle.danger)

        button.callback = interaction_a
        button2.callback = interaction_b
        view = View(button, button2)

        embed = discord.Embed(title="Hold up!", description=f"Are you sure you want to ban {member.mention}?")
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("Error!")


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"Successfuly cleared {amount} message(s).")


@client.command(aliases=["8ball", "eightball"])
async def _8ball(ctx, *, question):
    response = await get_response(type="8ball")

    embed = discord.Embed(title=f"{question}", color=app.config.c_main)
    # embed.add_field(name="Magic 8ball's response is:", value=f"{random.choice(responses_ball)}", inline=False)
    embed.add_field(name="Magic 8ball's response is:", value=f"{response}", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def fact(ctx):
    fact_url = "https://uselessfacts.jsph.pl/random.txt?language=en"

    fact = requests.get(fact_url)

    response = await get_response(type="normal")

    embed = discord.Embed(title=response, description=fact.text, color=app.config.c_main)
    await ctx.send(embed=embed)


@client.command()
async def joke(ctx):
    joke_url = "https://joke.jace.pro/.netlify/functions/jokes?random=true"

    joke = (requests.request("GET", joke_url).json())

    response = {
        "joke": joke["joke"],
        "punchline": joke["punchline"]
    }

    responses = await get_response(type="normal")

    embed = discord.Embed(title=responses,
                          description=f'> {response["joke"]}\n\n||{response["punchline"]}||', color=app.config.c_main)
    await ctx.send(embed=embed)


@client.command()
async def stats(ctx):
    member_count = len([m for m in ctx.guild.members if not m.bot])
    bot_count = len([m for m in ctx.guild.members if m.bot])
    embed = discord.Embed(title="Server statistics", color=app.config.c_main)
    embed.add_field(name="Members", value=f"{member_count}", inline=True)
    embed.add_field(name="Bots", value=f"{bot_count}", inline=True)
    await ctx.send(embed=embed)


@client.command()
async def credits(ctx):
    embed = discord.Embed(title="Credits", color=app.config.c_main)
    embed.add_field(name="Programmers:", value="Czebosak", inline=False)
    embed.add_field(name="Artists:", value="Czebosak", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def bunny(ctx):
    bunny_url = "https://api.bunnies.io/v2/loop/random/?media=gif,png"

    image = (requests.request("GET", bunny_url).json())
    
    response = await get_response(type="normal")

    responses = {
        "url": image["media"]["gif"],
        "source": image["source"]
    }

    embed = discord.Embed(title=response, color=app.config.c_main)
    embed.set_image(url=response["url"])
    embed.add_field(name="Source:", value=f'*{responses["url"]}*', inline=False)
    await ctx.send(embed=embed)


# @client.command()
# async def meme(ctx):
#    apikey = "1CXZJEMHK2GN"
#    lmt = 1
#
#    search_term = "meme"
#
#    r = requests.get("https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt)).json()
#
#    print(r)

@client.command(aliases=["dogs", "puppy", "puppies"])
async def dog(ctx, breed=" "):
    breed = breed.lower()

    if breed == "husky":
        dog_url = "https://dog.ceo/api/breed/husky/images/random"
    elif breed == "bulldog":
        dog_url = "https://dog.ceo/api/breed/bulldog/images/random"
    elif breed == "pug":
        dog_url = "https://dog.ceo/api/breed/pug/images/random"
    elif breed == "golden retriever" or breed == "golden_retriever":
        dog_url = "https://dog.ceo/api/breed/retriever/golden/images/random"
    elif breed == "retriever":
        dog_url = "https://dog.ceo/api/breed/retriever/images/random"
    elif breed == "shiba":
        dog_url = "https://dog.ceo/api/breed/shiba/images/random"
    elif breed == "puggle":
        dog_url = "https://dog.ceo/api/breed/puggle/images/random"
    elif breed == "poodle":
        dog_url = "https://dog.ceo/api/breed/poodle/images/random"
    elif breed == "mix":
        dog_url = "https://dog.ceo/api/breed/mix/images/random"
    else:
        dog_url = "https://dog.ceo/api/breeds/image/random"

    image = (requests.request("GET", dog_url).json())

    response = await get_response(type="normal")

    responses = {
        "url": image["message"]
    }

    embed = discord.Embed(title=response, color=app.config.c_main)
    embed.set_image(url=responses["url"])
    await ctx.send(embed=embed)


# @client.command(aliases=["cats", "kitten", "kittens"])
# async def cat(ctx, breed=" "):

@client.command()
@commands.has_role("Giveaways")
async def gstart(ctx):
    await ctx.send("Let's start with this giveaway! Anwser these questions within 15 seconds.")

    questions = [
        "Which channel should the giveaway be hosted in?",
        "What should be the duration of the giveaway? (S|M|H|D)",
        "What should be the price of the giveaway?"
    ]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for("message", timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You didn't answer the question in time.")
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly.")
        return

    channel = client.get_channel(c_id)

    time = app.config.convert(answers[1])
    if time == -1:
        await ctx.send("You didn't use a proper unit! Use S M H or D")
        return
    elif time == -2:
        await ctx.send("The time must be an integer.")
        return
    prize = answers[2]

    await ctx.send(f"The giveaway will be in the channel {channel.mention} and will last {time} seconds!")

    embed = discord.Embed(title="Giveaway!", description="React with 🎉 to join!")
    if len(prize) > 20:
        embed.add_field(name="Prize:", value=f"{prize}", inline=False)
    else:
        embed.add_field(name="Prize:", value=f"{prize}", inline=True)
    embed.add_field(name="Hosted by:", value=ctx.author.mention, inline=True)
    embed.set_footer(text=f"Ends in {answers[1]} from now!")

    my_msg = await channel.send(embed=embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    try:
        winner = random.choice(users)
    except IndexError:
        await channel.send("Nobody has entered the giveaway.")
        return

    await channel.send(f"Congratulations! {winner.mention} won {prize}!")


@client.command()
async def links(ctx):
    embed = discord.Embed(title="Links", description="Duh")
    embed.add_field(name="Discord server", value="https://discord.gg/bcp6dWdhcN", inline=False)
    embed.add_field(name="Invite the bot",
                    value="https://discord.com/api/oauth2/authorize?client_id=972575188166262815&permissions=1541859179766&scope=bot",
                    inline=False)

    await ctx.send(embed=embed)


################################
###         Economy          ###
################################


@client.command(aliases=["bal"])
async def balance(ctx):
    await app.config.open_account(ctx.author)

    user = ctx.author
    users = await app.config.get_bank_data()

    wallet_bal = users[str(user.id)]["wallet"]
    bank_bal = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{user.display_name}'s balance", color=app.config.c_main)
    embed.add_field(name="Wallet:", value=wallet_bal, inline=False)
    embed.add_field(name="Bank:", value=bank_bal, inline=False)
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 30, commands.cooldowns.BucketType.user)
async def beg(ctx):
    await app.config.open_account(ctx.author)

    user = ctx.author
    users = await app.config.get_bank_data()

    earnings = random.randint(90, 300)
    await app.config.update_bank_data(user, earnings)

    await ctx.send(f"You got {earnings}🍌 !")


@client.command()
async def withdraw(ctx, amount=None):
    await app.config.open_account(ctx.author)

    if amount is None:
        await ctx.send("Enter the amount to withdraw.")
        return

    bal = await app.config.get_specific_bank_data(ctx.author)

    amount = int(amount)
    if amount > bal[1]:
        await ctx.send("You don't have that much money in the bank.")
        return
    elif amount < 0:
        await ctx.send("The amount must be positive!")
        return
    elif amount == 0:
        await ctx.send("The amount cannot be equal to 0!")
        return

    await app.config.update_bank_data(ctx.author, amount, "wallet")
    await app.config.update_bank_data(ctx.author, -1 * amount, "bank")

    await ctx.send(f"You successfully withdrew {amount}🍌 !")


@client.command(aliases=["dep"])
async def deposit(ctx, amount=None):
    await app.config.open_account(ctx.author)

    if amount is None:
        await ctx.send("Enter the amount to deposit.")
        return

    bal = await app.config.get_specific_bank_data(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send("You don't have that much money in the wallet.")
        return
    elif amount < 0:
        await ctx.send("The amount must be positive!")
        return
    elif amount == 0:
        await ctx.send("The amount cannot be equal to 0!")
        return

    await app.config.update_bank_data(ctx.author, -1 * amount, "wallet")
    await app.config.update_bank_data(ctx.author, amount, "bank")

    await ctx.send(f"You successfully deposited {amount}🍌 !")


####################
## Slash commands ##
####################

@client.slash_command(guild_ids=[972791561450573824], name="balance", description="Check the balance of a user")
async def balance(ctx, user:
Option(
    discord.Member,
    "The user that you want to check the balance of",
    required=False,
    default=None
)):
    if user is None:
        user = ctx.author
    await app.config.open_account(user)

    users = await app.config.get_bank_data()

    wallet_bal = users[str(user.id)]["wallet"]
    bank_bal = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{user.display_name}'s balance", color=app.config.c_main)
    embed.add_field(name="Wallet:", value=app.config.format_number(wallet_bal), inline=False)
    embed.add_field(name="Bank:", value=app.config.format_number(bank_bal), inline=False)
    await ctx.respond(embed=embed)


@client.user_command(guild_ids=[972791561450573824], name="Balance")
async def balance(ctx, user: discord.Member):
    await app.config.open_account(user)

    users = await app.config.get_bank_data()

    wallet_bal = users[str(user.id)]["wallet"]
    bank_bal = users[str(user.id)]["bank"]

    embed = discord.Embed(title=f"{user.display_name}'s balance", color=app.config.c_main)
    embed.add_field(name="Wallet:", value=wallet_bal, inline=False)
    embed.add_field(name="Bank:", value=bank_bal, inline=False)
    await ctx.respond(embed=embed)


@client.user_command(guild_ids=[972791561450573824], name="Pickpocket", pass_context=True)
async def pickpocket(ctx, user: discord.Member):
    if ctx.author == user:
        await ctx.respond("You cannot rob yourself!")
    else:
        if True:

            # Check for the account of the author and of the user that is robbed
            await app.config.open_account(ctx.author)
            await app.config.open_account(user)
            bal = await app.config.get_specific_bank_data(user)
            robber = await app.config.get_specific_bank_data(ctx.author)

            # Check if the robber or the author has less  than 75k money
            if int(bal[0]) < 75000:
                await ctx.respond("The user has less than 75,000🍌!")
                return

            if int(robber[0]) < 75000:
                await ctx.respond("You need to have atleast 75,000🍌 to use this command!")
                return

            # Get the skill of the author
            level = await app.config.get_specific_user_skills(ctx.author, type="stealing")
            victim_level = await app.config.get_specific_user_skills(user, type="stealing")

            fail_chance = await app.config.calculate_chances(dfchance=667, level=level["level"], victim_lvl=victim_level["level"])


            # Calculate the amount of cash to steal from the player
            if level["level"] / 5 < 1:
                earnings = (random.randint(700, 3000) * (bal[0] / 10000)) / 100
            else:
                earnings = ((random.randint(700, 3000) * (bal[0] / 10000)) * level["level"] / 5) / 100

            earnings = round(earnings)

            if random.randint(0, 1000) > fail_chance:
                await app.config.update_bank_data(user, -1 * earnings, "wallet")
                await app.config.update_bank_data(ctx.author, earnings, "wallet")

                embed=discord.Embed(title="You stole:")
                embed.add_field(name="100🍌", value=f"from {user.mention}", inline=False)
                await ctx.respond(embed=embed)
            else:
                loss = earnings / 2

                await app.config.update_bank_data(ctx.author, -1 * loss , "wallet")

                embed=discord.Embed(title="You lost:")
                embed.add_field(name="100🍌", value=f"while trying to steal from {user.mention}", inline=False)
                await ctx.respond(embed=embed)
        else:
            await ctx.respond("The user you are trying to steal from isn't Online!")


@client.slash_command(guild_ids=[972791561450573824], name="embed", description="Check the balance of a user")
async def embed(ctx, title:
    Option(
        str,
        "The title of the embed",
        required=True
    ),
    description:
    Option(
        str,
        "The description of the embed",
        required=False,
        default=""
    ),
    color:
    Option(
        str,
        "The color of the embed",
        required=False,
        default=app.config.c_main,
        autocomplete=discord.utils.basic_autocomplete(app.config.colors)
    ),
    field_1_title:
    Option(
        str,
        "The title of the first field",
        required=False,
        default=None
    ),
    field_1_description:
    Option(
        str,
        "The title of the first field",
        required=False,
        default=None
    ),
    field_2_title:
    Option(
        str,
        "The title of the second field",
        required=False,
        default=None
    ),
    field_2_description:
    Option(
        str,
        "The title of the second field",
        required=False,
        default=None
    ),
    field_3_title:
    Option(
        str,
        "The title of the third field",
        required=False,
        default=None
    ),
    field_3_description:
    Option(
        str,
        "The title of the third field",
        required=False,
        default=None
    )
):

    if not color == app.config.c_main:
        color = app.config.color_convert[color]

    embed = discord.Embed(title=title, description=description, color=color)

    if field_1_title is not None and field_1_description is not None:
        embed.add_field(name=field_1_title, value=field_1_description, inline=False)
    if field_2_title is not None and field_2_description is not None:
        embed.add_field(name=field_2_title, value=field_2_description, inline=False)
    if field_3_title is not None and field_3_description is not None:
        embed.add_field(name=field_3_title, value=field_3_description, inline=False)

    await ctx.respond("Embed created!")

    await ctx.send(embed=embed)


@client.slash_command(guild_ids=[972791561450573824], name="config", description="description conf")
async def conf(ctx, mode:
    Option(
        str,
        "Show server's or user's config",
        required=True,
        autocomplete=discord.utils.basic_autocomplete(app.config.cfg_mode)
    ),
    setting:
    Option(
        str,
        "The setting that you want to change",
        required=False,
        default=None,
        autocomplete=discord.utils.basic_autocomplete(app.config.cfg_settings)
    ),
    value:
    Option(
        str,
        "The value that you want to change the setting to",
        required=False,
        default=None,
        autocomplete=discord.utils.basic_autocomplete(app.config.cfg_values)
    )
):
    if mode in app.config.cfg_mode:
        if mode == "Server":
            mode = "guilds"
        elif mode == "User":
            mode = "guilds"
        if setting in app.config.cfg_settings:
            if value in app.config.cfg_values:
                await app.config.config(id=ctx.user.id, value=value, mode="change", setting=setting, type=mode)
        elif setting is None:
            response = await app.config.config(id=ctx.user.id, value=value, mode="get", setting="safe")

            await ctx.respond(response)


client.run(app.config.TOKEN)
# https://discord.com/api/oauth2/authorize?client_id=972575188166262815&permissions=1644938390743&scope=applications.commands%20bot