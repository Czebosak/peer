from time import sleep
import discord
from discord.ext import commands, tasks
from ..config.tracers import get_all_data
from os import environ
from googleapiclient.discovery import build
#from twitchAPI import Twitch
from threading import Thread
from asyncio import sleep

youtube_api_key = environ.get("youtube_api_key")
twitch_api_id = environ.get("peer_twitch_api_client_id")
twitch_api_key = environ.get("peer_twitch_api_token")

#twitch = Twitch(twitch_api_id, twitch_api_key)

#user_info = twitch.get_users(logins=['czebosak'])

class tracers(commands.Cog):

    def __init__(self, client):
        self.client = client
    

    @tasks.loop(seconds=5)
    async def get_tracers(self):
        for id, data in get_all_data().items():
            print(data)

    
def setup(client):
    client.add_cog(tracers(client))
