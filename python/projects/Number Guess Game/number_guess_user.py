import random

def user_guess():
    low = 1
    high = 100
    attempts = 0
    
    secret_number = random.randint(low, high)  # Computer sets the number
    print("I have chosen a number between 1 and 100. Try to guess it!")
    
    while True:
        guess = int(input("Enter your guess: "))
        attempts += 1
        
        if guess == secret_number:
            print(f"Congratulations! You guessed the number {secret_number} in {attempts} attempts.")
            break
        elif guess > secret_number:
            print("Too high! Try again.")
        else:
            print("Too low! Try again.")

user_guess()