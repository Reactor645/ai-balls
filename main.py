import pygame
import random
import math
from ai import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

last_distance = 0
collision_reward = 10

last_move = None
last_target_direction = None

learning_rate = 0.1

current_balls = []

class Ball:
    def __init__(self, x, y, radius):

        self.x = x
        self.y = y
        self.radius = radius

def setup():
    global last_distance
    current_balls.clear()

    ball2x = random.randint(0, 1280)
    ball2y = random.randint(0, 720)

    ball1 = Ball(640, 360, 50)

    ball2 = Ball(ball2x, ball2y, 50)

    current_balls.append(ball1)
    current_balls.append(ball2)

    last_distance = math.hypot(current_balls[0].x - current_balls[1].x, current_balls[0].y - current_balls[1].y)

def check_collision(ball1, ball2):

    distance = math.hypot(
        ball1.x - ball2.x,
        ball1.y - ball2.y
    )

    return distance <= ball1.radius + ball2.radius

def move(direction):

    ai_ball = current_balls[0]

    if direction == "LEFT":
        ai_ball.x -= 10

    elif direction == "RIGHT":
        ai_ball.x += 10

    elif direction == "UP":
        ai_ball.y -= 10
    
    elif direction == "DOWN":
        ai_ball.y += 10


def check_if_closer():

    global last_distance

    distance = math.hypot(current_balls[0].x - current_balls[1].x, current_balls[0].y - current_balls[1].y)

    with open("memory.json") as f:
        data = json.load(f)

    reward = last_distance - distance


        

        
    if last_move == "UP":
        data[last_target_direction][0] += reward * learning_rate
    if last_move == "DOWN":
        data[last_target_direction][1] += reward * learning_rate
    if last_move == "LEFT":
        data[last_target_direction][2] += reward * learning_rate
    if last_move == "RIGHT":
        data[last_target_direction][3] += reward * learning_rate

    with open("memory.json", "w") as f:
        json.dump(data, f, indent=4)

    print(data)

    last_distance = distance
    
         
def exploration():

    global last_move

    explore_chance = random.randint(0, 10)

    if explore_chance == 1:
         possible_moves = ["UP", "DOWN", "LEFT", "RIGHT"]

         last_move = random.choice(possible_moves)

         print("EXPLORED!")


def tick():

    global last_move, last_target_direction, last_distance

    with open("memory.json") as f:
         data = json.load(f)

    for ball1 in current_balls:
        for ball2 in current_balls:
            if ball1 == ball2:
                continue

            if check_collision(ball1, ball2):
                print("Balls have collided!")
                if last_move == "UP":
                    data[last_target_direction][0] += collision_reward
                if last_move == "DOWN":
                    data[last_target_direction][1] += collision_reward
                if last_move == "LEFT":
                    data[last_target_direction][2] += collision_reward
                if last_move == "RIGHT":
                    data[last_target_direction][3] += collision_reward
                
                with open("memory.json", "w") as f:
                    json.dump(data, f, indent=4)
                setup()
                last_distance = math.hypot(current_balls[0].x - current_balls[1].x, current_balls[0].y - current_balls[1].y)
                return

            else:
                continue

    chosen_move, last_target_direction = choose_move(
        current_balls[0].x,
        current_balls[0].y,
        current_balls[1].x,
        current_balls[1].y
    )

    last_move = chosen_move.upper()
    exploration()
    move(last_move)
    check_if_closer()




    
    
    

    



setup()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move("LEFT")
        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        move("RIGHT")
        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        move("UP")
        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        move("DOWN")

    screen.fill("black")


    for ball in current_balls:

        pygame.draw.circle(screen, (255, 255, 255), (ball.x, ball.y), ball.radius)

    tick()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()