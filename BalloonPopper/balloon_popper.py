from turtle import *
import random

diameter = 40
pop_diameter = 100

def change_color():
    r = random.random()
    g = random.random()
    b = random.random()
    color(r, g, b)

def draw_balloon():
    change_color()
    dot(diameter)

def inflate_balloon():
    global diameter
    diameter = diameter + 10
    draw_balloon()

    if diameter >= pop_diameter:
        clear()
        diameter = 40
        write("POP!")

def deflate_balloon():
    global diameter
    diameter -= 5
    clear()
    draw_balloon()

    if diameter < 10:
        diameter = 40

draw_balloon()
onkey(inflate_balloon, "Up")
onkey(deflate_balloon, "Down")
listen()

exitonclick()

