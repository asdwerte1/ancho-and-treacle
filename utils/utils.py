from json import load

def read_config(config_path: str):
    with open(config_path, "r") as config:
        config_data = load(config)
        return config_data