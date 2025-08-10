import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''
game_list=[rock,paper,scissors]
your_choice=int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors. \n"))
if your_choice<=3 and your_choice>0:
     print(game_list[your_choice])
ai=random.randint(0,2)
print('computer choose:')
print(game_list[ai])
if your_choice >= 3 or your_choice < 0:
    print("you typed an invalid number")
elif ai==your_choice:
    print('It\'s a draw!')
elif ai>your_choice:
    print("You win")
elif ai<your_choice:
    print("You lose")
elif ai==0 and your_choice==2:
    print("You lose")
elif ai==2 and your_choice==0:
    print("You win")
