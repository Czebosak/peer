from json import load

def get_all_servers():
    with open("app/data/tracers.json", "r") as f:
        return list(load(f).keys())

def get_all_data():
    with open("app/data/tracers.json", "r") as f:
        return load(f)
