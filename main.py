import time
from tkinter import *
import random

from fuzzylogic import compute


def generate_new_obstacle(can, width, obstacle_table):
    centre = random.randint(30, width-30)

    x0 = centre - random.randint(10, 31)
    x1 = centre + random.randint(10, 31)

    y0 = -random.randint(10, 40)
    y1 = -random.randint(10, 30)

    rect = can.create_rectangle(x0, y0, x1, y1, fill="brown")
    obstacle_table.append(rect)
    print(obstacle_table)


def move_obstacles(c, speed, obstacle_table):
    for item in obstacle_table:
        c.move(item, 0, speed)


def calc_dist_from_obstacle(my_coords, obstacle_coords):
    # do I see an obstacle:
    my_x0 = my_coords[0]
    my_y0 = my_coords[1]
    my_x1 = my_coords[2]

    ob_x0 = obstacle_coords[0]
    ob_y0 = obstacle_coords[1]
    ob_x1 = obstacle_coords[2]

    if ( (ob_x0 <= my_x0 <= ob_x1) or (ob_x0 <= my_x1 <= ob_x1) ) and ob_y0 <= 398 :
        return my_y0 - ob_y0
    else:
        return 399


def calc_dist_from_nearest_wall(my_coords, width):
    global current_direction
    my_x0 = my_coords[0]
    my_x1 = my_coords[2]


    left_wall_dist = my_x0
    right_wall_dist = width - my_x1

    print("Left wall distance")
    print(left_wall_dist)

    print ("Right wall distance")
    print(right_wall_dist)

    res = min(left_wall_dist, right_wall_dist)

    if right_wall_dist < 10:
        current_direction = "-"

    elif left_wall_dist < 10:
        current_direction = "+"

    print(current_direction)
    return res



def get_first_visible_obstacle(canvas, my_ball, obstacle_table):
    for item in obstacle_table:
        ob_dist = calc_dist_from_obstacle(canvas.coords(my_ball), canvas.coords(item))
        if ob_dist < 399:
            return item
    return canvas.create_rectangle(0,0,0,0)


current_direction = ""

def main():

    obstacle_table = []

    # Program parameters:
    obstacle_speed = 5
    update_interval = 0.02
    width = 500
    height = 400

    animation = Tk()
    animation.title("Fuzzy Logic Visualizer")

    canvas = Canvas(animation, width=width, height=height)
    canvas.pack()
    canvas.configure(background="lightgrey")

    # The ball that wants to avoid the obstacles:
    ball = canvas.create_oval(240, 370, 260, 390, fill="red")
    print(canvas.coords(ball))

    # Counter for interval to generate new obstacle:
    counter = 0

    # Initial speed of the ball
    shift = 0

    while True:

        # 1. Move the obstacle(s):
        move_obstacles(canvas, obstacle_speed, obstacle_table)

        # 2. Assess the situation:
        #   2a get the obstacle distance:
        visible = get_first_visible_obstacle(canvas, ball, obstacle_table)
        print(canvas.coords(visible))

        obstacle_distance = calc_dist_from_obstacle(canvas.coords(ball), canvas.coords(visible))
        print(obstacle_distance)


        #   2b get the wall distance:
        nearest_wall_distance = calc_dist_from_nearest_wall(canvas.coords(ball), 500)
        print("Distance to wall:")
        print(nearest_wall_distance)


        # 3. Calculate the move:
        shift = compute(obstacle_distance, nearest_wall_distance, shift)
        print(shift)
        print("\n")

        if current_direction == "-":
            shift = -shift

        # 3. Move the ball:
        canvas.move(ball, shift, 0)


        # 4. Update the animation
        counter+=1
        if counter == 50:
            generate_new_obstacle(canvas, width, obstacle_table)
            counter = 0
            #clean_up_obstacle_table()

        animation.update()
        time.sleep(update_interval)



if __name__ == '__main__':
    main()
