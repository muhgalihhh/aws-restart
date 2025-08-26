import random

def number_guessing_game():
    print("Welcome to Guess the Number!")
    print("The rules are simple. I will think of a number, and you will try to guess it.")
    
    number = random.randint(1, 10)
    max_attempts = 5
    attempts = 0
    is_guess_right = False
    
    while not is_guess_right and attempts < max_attempts:
        try:
            guess = input(f"Guess a number between 1 and 10 (attempt {attempts + 1}/{max_attempts}): ")
            guess_num = int(guess)
            
            if guess_num < 1 or guess_num > 10:
                print("Please enter a number between 1 and 10.")
                continue
                
            attempts += 1
            
            if guess_num == number:
                print(f"You guessed {guess_num}. That is correct! You win!")
                print(f"You found it in {attempts} attempts!")
                is_guess_right = True
            else:
                if guess_num < number:
                    print(f"You guessed {guess_num}. Too low! Try again.")
                else:
                    print(f"You guessed {guess_num}. Too high! Try again.")
                    
        except ValueError:
            print("Please enter a valid number.")
            continue
    
    if not is_guess_right:
        print(f"Game over! The number was {number}.")

if __name__ == "__main__":
    number_guessing_game()