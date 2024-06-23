
# * display - display name of the job
# * work_xp_join - work expierence that the user gets when joining the job
# * work_xp - work expierence that the user gets when they work (users can only work once per hour)
# * money - salary
# * requirement - work experience to get hired
# * temp - Should this be a part time job?
# Part time job

jobs = {
    "delivery": {
        "display": "Delivery Person",
        "work_xp_join": [0, 0],
        "work_xp": [3, 8],
        "money": [200, 300],
        "requirement": 0,
        "temp": True
    },
    "shop_assistant" : {
        "display": "Shop Assistant",
        "work_xp_join": [20, 40],
        "work_xp": [5, 20],
        "money": [350, 450],
        "requirement": 0,
        "temp": False
    },
    "banker" : {
        "display": "Banker",
        "work_xp_join": [40, 80],
        "work_xp": [20, 35],
        "money": [600, 650],
        "requirement": 300,
        "temp": False
    },
    "programmer": {
        "display": "Programmer",
        "work_xp_join": [300, 400],
        "work_xp": [40, 80],
        "money": [2000, 2700],
        "requirement": 10000,
        "temp": False
    }
}
