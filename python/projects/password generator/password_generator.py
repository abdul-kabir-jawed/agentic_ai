import random

def generate_password(letters, numbers, symbols):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    digits = '0123456789'
    special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?/'
    
    password_chars = (
        random.choices(alphabet, k=letters) +
        random.choices(digits, k=numbers) +
        random.choices(special_chars, k=symbols)
    )
    
    random.shuffle(password_chars)
    return ''.join(password_chars)

letters = int(input("Enter number of letters: "))
numbers = int(input("Enter number of digits: "))
symbols = int(input("Enter number of symbols: "))

print("Generated password:", generate_password(letters, numbers, symbols))