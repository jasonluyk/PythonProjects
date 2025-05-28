from turtle import *
from random import *

#setting the background color and hiding the turtle
bgcolor("black")
hideturtle()

#speeding up the star generation
speed(0)

#establishing the width and height of the screen
width = window_width()
height = window_height()

#function to draw the stars
def draw_star(x_pos, y_pos):
    size = randrange(4, 20)
    penup()
    goto(x_pos, y_pos)
    pendown()
    dot(size, "white")

#loop used to randomly generate the stars on the screen
for i in range(150):
    x_pos = randrange(-width // 2, width // 2)
    y_pos = randrange(-height // 2, height // 2)
    draw_star(x_pos, y_pos)





exitonclick()
