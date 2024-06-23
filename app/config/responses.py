import random

responses = (
    "Sure!",
    "Lemme find something...",
    "Here's a good one!"
)

responses_ball = (
    "As I see it, yes.",
    "Don’t count on it.",
    "It is certain.",
    "It is decidedly so.",
    "Most likely.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Outlook good.",
    "Signs point to yes.",
    "Very doubtful.",
    "Without a doubt.",
    "Yes.",
    "Yes – definitely.",
    "You may rely on it."
)

responses_beg = (
    '"You poor little beggar"',
    '"Here"',
    "a person passes by and drops you some money"
)

responses_beg_a = (
    '"Get a job!"',
    '"Go get a job!"',
    "No one wanted to give you money"
)

responses_cooldown = (
    "Hold your horses!",
    "Slow down!",
    "Take it easy!",
    "Hey!"
)


def get_response(type="normal"):
    if type == "normal":
        response = responses
    elif type == "8ball":
        response = responses_ball
    elif type == "beg":
        response = responses_beg
    elif type == "cooldown":
        response = responses_cooldown
    else:
        response = responses

    return random.choice(response)
