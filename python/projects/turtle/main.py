from turtle import Turtle, Screen
import random

colors=["red", "orange", "yellow", "green", "blue", "purple"]
y_coordinates=[-150,-100,-50,0,50,100]

is_race_on=False

screen=Screen()
screen.setup(width=500, height=400)
user_bet = None
while user_bet not in colors:
    user_bet = screen.textinput("Make your bet", 
        f"Which turtle will win the race? Choose from: {','.join(colors)}").lower()
all_turtles=[]

for turle_index in range(6):
  new_turtle=Turtle(shape="turtle")
  new_turtle.color(colors[turle_index])
  new_turtle.penup()
  new_turtle.goto(-230, y_coordinates[turle_index])
  all_turtles.append(new_turtle)

if user_bet:
  is_race_on=True

while is_race_on:
   
    for turtle in all_turtles:
      if turtle.xcor()>230:
        is_race_on=False
        winning_color=turtle.pencolor()
        if winning_color==user_bet:
          print(f"You've won! The {winning_color} turtle is the winner!")
        else:
          print(f"You've lost! The {winning_color} turtle is the winner!")
      turtle_distance=random.randint(0, 10)
      turtle.forward(turtle_distance)

screen.exitonclick()