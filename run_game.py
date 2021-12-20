import yaml
import argparse
from typing import Tuple, Dict

def load_configs(game_config_path: str) -> Tuple[str, str]:
    # Load the game config
    with open(game_config_path, "r") as game_config_stream:
        game_config = yaml.safe_load(game_config_stream)

    # Load the room configs
    room_configs = dict()
    for room_name, room_config_path in game_config["rooms"].items():
        with open(room_config_path, "r") as room_config_stream:
            room_configs[room_name] = yaml.safe_load(room_config_stream)
    
    return game_config, room_configs

def run_game(room_configs: Dict, init_room: str, init_state: str, exit_game_state: str="FIN") -> None:
    current_room = init_room
    current_state = init_state

    while(current_state != exit_game_state):
        # Extract outputs and action choices from room config
        room_config = room_configs[current_room]
        room_current_state_config = room_config["states"][current_state]
        output_text = room_current_state_config["output"]
        action_choices = room_current_state_config["actions"]
        action_text = list(action_choices.keys())

        if "leave_room_allowed" in room_current_state_config and room_current_state_config["leave_room_allowed"]:
            leave_room_choices = room_config["leave_room"]
            leave_room_text = list(leave_room_choices.keys())
        else:
            leave_room_text = []

        # Interactions
        print(output_text)
        proceed_to_next = False
        while not proceed_to_next:
            action = input("-- Please select one of these actions: %s\n>> " % (action_text + leave_room_text))
            if action in action_text:
                proceed_to_next = True
                current_state = action_choices[action]
            elif action in leave_room_text:
                proceed_to_next = True
                current_room = leave_room_choices[action]["room"]
                current_state = leave_room_choices[action]["state"]
            else:
                print("'%s' is not a valid choice." % action)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Play an adventure game!")
    parser.add_argument("game_config_path", type=str,
                        help="Path to game's config yaml file")
    args = parser.parse_args()

    game_config, room_configs = load_configs(args.game_config_path)
    
    init_room = game_config["init_room"]
    init_state = game_config["init_state"]
    run_game(room_configs, init_room, init_state)
