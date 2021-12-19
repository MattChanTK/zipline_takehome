import yaml
import sys
import argparse


parser = argparse.ArgumentParser(description="Play an adventure game!")
parser.add_argument("game_config_path", type=str,
                    help="Path to game's config yaml file")
args = parser.parse_args()

# Read config YAML file
with open(args.game_config_path, "r") as game_config_stream:
    game_config = yaml.safe_load(game_config_stream)

# Loading the room configs
room_configs = dict()
for room_name, room_config_path in game_config["rooms"].items():
    with open(room_config_path, "r") as room_config_stream:
        room_configs[room_name] = yaml.safe_load(room_config_stream)

print(room_configs)

