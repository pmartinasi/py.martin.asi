import pyautogui
import time
import random

def alternate_clicks():
    # A variable to track the last click type (True for left click, False for right click)
    last_left_click = True
    
    while True:
        # Generate a random sleep time between 10 and 20 seconds
        wait_time = random.uniform(10, 20)
        print(f"Waiting for {wait_time:.2f} seconds before next click.")
        
        # Wait for the random duration
        time.sleep(wait_time)
        #pyautogui.rightClick()
        pyautogui.leftClick()

        # Perform the click (alternating between right and left)
        #if last_left_click:
        #    pyautogui.rightClick()
        #else:
        #    pyautogui.leftClick()
        
        # Toggle the click for the next iteration
        last_left_click = not last_left_click

if __name__ == "__main__":
    print("Starting alternate clicks with random intervals between 30 and 45 seconds.")
    alternate_clicks()
