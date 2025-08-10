import random

def computer_guess():
    low = 1
    high = 100
    attempts = 0
    
    secret_number = int(input("Choose a number between 1 and 100 for me to guess: "))  # User sets the number
    print("Great! Now I'll try to guess it.")
    
    while True:
        guess = random.randint(low, high)
        attempts += 1
        print(f"I guess {guess}")
        
        if guess == secret_number:
            print(f"Yay! I guessed it right: {guess} in {attempts} attempts.")
            break

        elif guess!=secret_number:
            user=input("Is the number high or low?").lower()
            if user=="high":
                print("High! I'll guess lower.")
                high=guess-1
            elif user=="low":
                print("low! I'll guess higher.")
                low=guess+1
        # elif guess > secret_number:
        #     print("Too high! I'll guess lower.")
        #     high = guess - 1
        # else:
        #     print("Too low! I'll guess higher.")
        #     low = guess + 1

computer_guess()