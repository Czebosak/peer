import json
from os import environ
from easy_pil import Canvas, Editor, Font
from io import BytesIO

TOKEN = environ.get("PEER_TOKEN")

c_main = 0x102b3f

color_convert = {
    "blue": 0x3498db,
    "blurple": 0x5865F2,
    "brand_green": 0x57F287,
    "brand_red": 0xED4245,
    "dark_blue": 0x206694,
    "dark_gold": 0xf1c40f,
    "dark_gray": 0x607d8b,
    "dark_green": 0x1f8b4c,
    "dark_magenta": 0xe91e63,
    "dark_orange": 0xa84300,
    "dark_purple": 0x71368a,
    "dark_red": 0x992d22,
    "dark_teal": 0x11806a,
    "dark_theme": 0x36393F,
    "darker_gray": 0x546e7a,
    "fuchsia": 0xEB459E
}

colors = (
    "blue",
    "blurple",
    "brand_green",
    "brand_red",
    "dark_blue",
    "dark_gold",
    "dark_gray",
    "dark_green",
    "dark_magenta",
    "dark_orange",
    "dark_purple",
    "dark_red",
    "dark_teal",
    "dark_theme",
    "darker_gray",
    "fuchsia"
)

emojis = {
    "mushroom": "<:brown_mushroom:991985316925820968>",
    "checkmark": "<:peer_checkmark:978689943410991114>",
    "x": "<:peer_x:978689943205470288>",
    "wip": "<:wip:992100490961756160>"
}

cfg_mode = (
    "Server",
    "User"
)

cfg_settings = (
    "Swear",
    "User"
)

cfg_values = (
    "True",
    "False"
)

fonts = {
    "poppins": Font("app/assets/fonts/poppins.ttf", size=44),
    "poppins-light": Font("app/assets/fonts/poppins-light.ttf", size=44),
    "poppins_small": Font("app/assets/fonts/poppins.ttf", size=36)
}

def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]


def format_number(number):
    formated_number = "{:,}".format(int(number))
    return formated_number


def duration(date, date2):
    delta = date - date2
    return delta.seconds


def convert_to_rgb(hex):
    rgb = tuple(int(str(hex).lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

    return rgb


async def config(id, value, mode="change", setting=None, type="users"):
    with open("app/data/config.json", "r") as f:
        com_data = json.load(f)

    if not str(id) in com_data:
        if mode == "get":
            return None
        else:
            if type == "guilds":
                com_data[type][str(id)] = {}
                com_data[type][str(id)]["safe"] = "True"
                com_data[type][str(id)]["verify"] = "True"
    else:
        if mode == "get":
            return com_data[type][str(id)][setting]
        elif mode == "change":
            com_data[type][str(id)][setting] = value

            with open("app/data/config.json", "w") as f:
                json.dump(com_data, f)

    com_data[type][str(id)][setting] = value

################################
###         Economy          ###
################################


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 5000
        users[str(user.id)]["bank"] = 0

    with open("app/data/balance.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("app/data/balance.json", "r") as f:
        users = json.load(f)

    return users


async def get_specific_bank_data(user):
    users = await get_bank_data()

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]

    return bal


async def update_bank_data(user, change, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] = int(users[str(user.id)][mode]) + change

    with open("app/data/balance.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]

    return bal


async def get_skills():
    with open("app/data/skills.json", "r") as f:
        users = json.load(f)

    return users


async def get_specific_user_skills(user, type="all"):
    users = await get_skills()

    if not str(user.id) in users:
        users[str(user.id)] = {}
        users[str(user.id)]["level"] = 1
        users[str(user.id)]["xp"] = 0
        users[str(user.id)]["work"] = {}
        users[str(user.id)]["work"]["current"] = "none"
        users[str(user.id)]["work"]["work_date"] = "none"
        users[str(user.id)]["work"]["work_xp"] = 0
        users[str(user.id)]["stealing"] = {}
        users[str(user.id)]["stealing"]["level"] = 1
        users[str(user.id)]["stealing"]["xp"] = 0
        users[str(user.id)]["charisma"] = {}
        users[str(user.id)]["charisma"]["level"] = 1
        users[str(user.id)]["charisma"]["xp"] = 0

        with open("app/data/skills.json", "w") as f:
            json.dump(users, f)

    if type == "all":
        skills = users[str(user.id)]
    elif type == "main":
        skills = [users[str(user.id)]["level"], users[str(user.id)]["xp"]]
    elif type == "work":
        skills = [users[str(user.id)]["work"]["work_xp"], users[str(user.id)]["work"]["current"], users[str(user.id)]["work"]["work_date"]]
    else:
        skills = users[str(user.id)][type]

    return skills


async def get_max_xp(level):
    multiplier = 1.1
    loop = 0
    max_xp = 181

    while loop < level:
        max_xp *= multiplier

        multiplier *= 1.03

        loop += 1
    
    return round(max_xp)


async def add_xp(user, xp=None, level=None):
    users = await get_skills()

    if int(users[str(user.id)]["level"]) == 100:
        return False;
    
    if xp is not None:
        max_xp = await get_max_xp(level=int(users[str(user.id)]["level"]))

        users[str(user.id)]["xp"] = int(users[str(user.id)]["xp"]) + xp

        if max_xp <= users[str(user.id)]["xp"]: 
            additional_xp = users[str(user.id)]["xp"] - max_xp
            
            if additional_xp > 0:
                users[str(user.id)]["xp"] = additional_xp
            else:
                users[str(user.id)]["xp"] = 0

            users[str(user.id)]["level"] += 1
            
            with open("app/data/skills.json", "w") as f:
                json.dump(users, f)

            return True;
            
        with open("app/data/skills.json", "w") as f:
            json.dump(users, f)

        return False;


async def calculate_chances(dfchance, level, lvldifference=None, victim_lvl=None):
    fnchance = dfchance

    if victim_lvl is not None and lvldifference is None:
        difference = (level - victim_lvl) * 10
        
        if difference > 300:
            difference = 300
        elif difference < -300:
            difference = -300

        fnchance - difference
    else:
        lvldifference *= -1
        
        while level > 0:
            fnchance *= lvldifference

            level -= 1

    fnchance = round(fnchance)

    return fnchance


#########
# ranks #
ranks = {
    "stealing": {
        "1": "pocket thief",
        "25": "smuggler",
        "50": "bandit",
        "100": "crime mastermind"
    },
    "charisma": {
        "1": "talker",
        "25": "babbler",
        "100": "negotiator"
    }
}
#       #
#########

async def stat(user, stat, action="modify", to=None, guild=None):
    with open("app/data/stats.json", "r") as f:
        users = json.load(f)

    if str(user.id) not in users:
        users[str(user.id)] = {}
        users[str(user.id)]["messages_sent"] = []
        users[str(user.id)]["messages_sent"].append(0)
        users[str(user.id)]["messages_sent"].append({})
        users[str(user.id)]["warnings"] = []

        with open("app/data/stats.json", "w") as f:
            json.dump(users, f)

    if action == "modify":
        if stat == "warnings":
            if len(users[str(user.id)]["warnings"]) >= 15:
                return False
            else:
                users[str(user.id)]["warnings"].append(to)

                with open("app/data/stats.json", "w") as f:
                    json.dump(users, f)
        else:
            users[str(user.id)][stat][0] += to

            if guild is not None:
                if str(guild.id) not in users[str(user.id)][stat][1]:
                    users[str(user.id)][stat][1][str(guild.id)] = 0

                users[str(user.id)][stat][1][str(guild.id)] += to

            with open("app/data/stats.json", "w") as f:
                json.dump(users, f)
    elif action == "get":
        return users[str(user.id)][stat]

async def generate_rank_card(user):
    canvas = Canvas((920, 380), color=(34, 47, 53))
    pfp = Editor(image=BytesIO(await user.display_avatar.read())).resize((150, 150)).circle_image()

    data = await get_specific_user_skills(user=user, type="main")
    level = data[0]
    xp = data[1]

    max_xp = await get_max_xp(level=level)

    progress = round((xp / max_xp) * 800)
    progress_left = (progress * -1) + 800
    progress_show = round((xp / max_xp) * 100)

    peer = (16, 43, 63)

    editor = Editor(canvas)
    editor.rectangle((20, 20), 880, 340, color=(54, 57, 63))
    editor.text(position=(40, 150), text=f"{user.display_name}#{user.discriminator}", font=fonts["poppins"], color="white")
    editor.text(position=(40, 192), text=f"Level {level}", font=fonts["poppins_small"], color="white")
    editor.text(position=(40, 217), text=f"{xp}/{max_xp} XP", font=fonts["poppins_small"], color="white")
    editor.text(position=(840, 217), text=f"{progress_show}%", font=fonts["poppins"], color="white", align="right")
    if progress_left <= 35:
        editor.rectangle((40, 260), 800, 70, color=(68, 71, 77), radius=35)
        editor.rectangle((40, 260), progress, 70, peer, radius=35)
    else:
        editor.rectangle((40, 260), 800, 70, peer, radius=35)
        editor.rectangle((progress + 40, 260), progress_left, 70, color=(68, 71, 77), radius=35)
        if progress >= 35:
            editor.rectangle((progress + 40, 260), 35, 70, color=(68, 71, 77))
    
    editor.paste(image=pfp.image, position=(40, 0))

    return editor
