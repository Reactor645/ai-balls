import json

def find_position(own_x, own_y, target_x, target_y):
    position = []

    if target_x > own_x:
        position.append("right")
    elif target_x < own_x:
        position.append("left")

    if target_y < own_y:
        position.append("up")
    elif target_y > own_y:
        position.append("down")

    return "_".join(position)


def choose_move(own_x, own_y, target_x, target_y):

    position = find_position(own_x, own_y, target_x, target_y)

    

    print("Detected position:", repr(position))
    print("Own coordinates:", own_x, own_y)
    print("Target coordinates:", target_x, target_y)

    with open("memory.json") as f:
        memory = json.load(f)

    if position not in memory:
        print(f"Unknown location: {position}")
        exit(69)

    memory = memory[position]

    moves = ["up", "down", "left", "right"]

    highest_rated_move = moves[0]
    highest_rated_move_score = float("-inf")

    for index, score in enumerate(memory):
        if score > highest_rated_move_score:
            highest_rated_move_score = score
            highest_rated_move = moves[index]

    print(f"Chose move {highest_rated_move} with score {highest_rated_move_score}")

    return highest_rated_move, position
