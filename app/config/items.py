from json import load, dump
from operator import inv
from ..config import emojis

items = [
    {
        "name": "Debit Card",
        "icon": "💳",
        "description": "Lorem ipsum.",
        "uuid": "3495b0fe-2b63-4316-abf7-c0fcde4d99f8",
        "price": [100000],
        "tags": ["non-tradable", "non-markatable"],
        "buyable": True,
        "sellable": False
    },
    {
        "name": "Common Fish",
        "icon": "🐟",
        "description": "It's a fish.",
        "uuid": "e62bbd2c-8a8f-4395-97d8-a2982d0c552b",
        "price": [360, 276],
        "tags": ["non-tradable", "non-markatable"],
        "buyable": False,
        "sellable": True
    },
    {
        "name": "Rare Fish",
        "icon": "🐠",
        "description": "It's like a fish, but rare.",
        "uuid": "1b686c35-0d90-454f-bb9c-8ff4be833c9d",
        "price": [1200, 840],
        "tags": ["non-tradable", "non-markatable"],
        "buyable": False,
        "sellable": True
    },
    {
        "name": "Blowfish",
        "icon": "🐡",
        "description": "Lorem ipsum.",
        "price": [2400, 1440],
        "tags": ["non-tradable", "non-markatable"],
        "uuid": "affdce23-e2a8-40e6-89c1-d42fa99d97460",
        "buyable": False,
        "sellable": True
    },
    {
        "name": "Shrimp",
        "icon": "🦐",
        "description": '*"Remember to remove the shell!"*',
        "uuid": "3b5d6d53-e21f-4a4e-aaed-9b4cdeefaae2",
        "price": [3000, 2000],
        "tags": ["non-tradable", "non-markatable"],
        "buyable": False,
        "sellable": True
    },
    {
        "name": "Mushroom",
        "icon": emojis["mushroom"],
        "description": "Consume to gain a random non-permament boost.",
        "uuid": "e15d4597-56ba-4816-a771-032aab75bc94",
        "price": [1000, 2000],
        "tags": ["non-tradable", "non-markatable", "consumable"],
        "buyable": False,
        "sellable": True
    },
    {
        "name": "Hunting Rifle",
        "icon": emojis["wip"],
        "description": "Enables hunting.",
        "uuid": "00667545-2ba8-41bb-bbbc-3e8b7bc86a97",
        "price": [10000],
        "tags": ["non-tradable", "non-markatable"],
        "buyable": True,
        "sellable": False
    },
    {
        "name": "Golden Rabbit",
        "icon": emojis["wip"],
        "description": 'Awarded to the best of the best.\n> *"Some say it comes from the era of Lord Rabbit."*',
        "uuid": "fe69337c-981a-4314-b04b-fff6df54c4f0",
        "tags": ["tradable", "non-markatable"],
        "buyable": False,
        "sellable": False
    },
    {
        "name": "Fishing Rod",
        "icon": emojis["wip"],
        "description": 'Awarded to the best of the best.\n> *"Some say it comes from the era of Lord Rabbit."*',
        "uuid": "fe69337c-981a-4314-b04b-fffsdf54c4f0", # Change
        "price": [10000],
        "tags": ["non-tradable", "non-markatable"],
        "buyable": True,
        "sellable": False
    }
]

async def get_inventories(object="player", id=None):
    with open("app/data/items.json", "r") as f:
        inventories = load(f)
        
    if id is not None and str(id) not in inventories["player_inventories"]:
        inventories["player_inventories"][str(id)] = []
        
        with open("app/data/items.json", "w") as f:
            dump(inventories, f)
    
    return inventories


async def get_inventory(inventory="inventory", object="player", id=None):
    inventories = await get_inventories(object, id)
    
    if object == "player": 
        if inventory == "inventory" or inventory == "player_inventories":
            return inventories["player_inventories"][str(id)]


async def get_item(item_id, by="name", inventory=None, id=None):
    if by == "name":
        if inventory == None:
            for item in items:
                if item_id.lower() in item["name"].lower():
                    return item;
            
            return False;
        else:
            i = await get_inventory(inventory="player_inventories", id=id)

            for item in i:
                if item_id in item:
                    return True;
            
            return False;
    elif by == "buyable":
        itemlist = []

        for i in items:
            if i["buyable"] is True:
                itemlist.append(i)
        
        return itemlist;
    elif by == "uuid":
        if inventory == None:
            for item in items:
                if str(item_id) == item["uuid"]:
                    return item;

            return False;
        else:
            i = await get_inventory(inventory, id=id)
            
            for item in i:
                if item_id in item:
                    return item;
            
            return False;


async def add_item(item, invtype="player", inventory="inventory", id=None):
    inventory = await get_inventories(id=str(id))

    if invtype == "player":
        inventory["player_inventories"][str(id)].append(item)

    with open("app/data/items.json", "w") as f:
        dump(inventory, f)


async def remove_item(item, invtype="player", inventory="inventory", id=None):
    inventory = await get_inventories(id=str(id))

    if invtype == "player":
        try:
            inventory["player_inventories"][str(id)].remove(item["uuid"])
        except ValueError:
            return False;

    with open("app/data/items.json", "w") as f:
        dump(inventory, f)