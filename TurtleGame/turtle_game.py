from turtle import *
import time

#setting speed
speed(0)

#setting our moving distance
move_distance = 50

#setting our sand background color 
bgcolor("#D2691E")

#setting our screen size for filling
width = window_width()
height = window_height()

#going to the ocean start point, lifting and dropping the pen
#penup()
#goto(width // 4, height // 2)
#pendown()


def fill_ocean():
    penup()
    goto(width // 4, height // 2)
    pendown()

    #starting our fill color
    color("blue")

    #fill zone
    begin_fill()
    goto(width // 2, height // 2)
    goto(width // 2, -height // 2)
    goto(width // 4, -height // 2)
    goto(width // 4, height // 2)
    end_fill()

#turtle start point
def turtle_start():
    penup()
    goto(-width // 4, 0)
    color("green")
    shape("turtle")

#movement of the turtle
def move_up():
    setheading(90)
    forward(move_distance)
    check_goal()
    check_boundaries()

def move_down():
    setheading(270)
    forward(move_distance)
    check_goal()
    check_boundaries()

def move_left():
    setheading(180)
    forward(move_distance)
    check_goal()
    check_boundaries()

def move_right():
    setheading(0)
    forward(move_distance)
    check_goal()
    check_boundaries()

#checking for completion and restarting the game
def check_goal():
    if xcor() > width // 4:
        hideturtle()
        color("white")
        write("YOU WIN!")
        time.sleep(1)
        clear()
        fill_ocean()
        showturtle()
        turtle_start()

#checking for out of bounds
def check_boundaries():
    if xcor() < -width // 2:
        turtle_start()
    elif ycor() > height // 2:
        turtle_start()
    elif ycor() < -height // 2:
        turtle_start()

fill_ocean()
turtle_start()
onkey(move_up, "Up")
onkey(move_down, "Down")
onkey(move_left, "Left")
onkey(move_right, "Right")
listen()



exitonclick()
