import time

def countdown_timer(minutes):
    seconds = minutes * 60
    input("Press Enter to start the countdown...")
    while seconds > 0:
        print(f"Time left: {seconds} seconds")
        time.sleep(1)
        seconds -= 1
    print("Time's up!")

minutes = int(input("Enter countdown time in minutes: "))
countdown_timer(minutes)