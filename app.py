import time
import random
import os
import threading
import sys

if os.name == 'nt':
    import msvcrt  # Import msvcrt for Windows

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_text():
    texts = [
        "The quick brown fox jumps over the lazy dog. This pangram contains every letter of the English alphabet at least once. Pangrams are often used to display fonts or test keyboards.",
        "Python is a versatile programming language known for its simplicity and readability. It supports multiple programming paradigms, including procedural, object-oriented, and functional programming.",
        "Practice makes perfect when it comes to typing. Regular typing exercises can significantly improve your speed and accuracy. Many online platforms offer typing games and tests to help you enhance your skills.",
        "Coding is both an art and a science. While it requires logical thinking and problem-solving skills, it also involves creativity in designing elegant solutions. Good code is not just about functionality; it should be readable, maintainable, and efficient.",
        "Efficiency and accuracy are key in typing tests. However, it's important to remember that improving your typing skills is a gradual process. Don't get discouraged if you don't see immediate results."
    ]
    return random.choice(texts)

def calculate_wpm(text, elapsed_time, user_input):
    correct_words = sum(1 for orig, typed in zip(text.split(), user_input.split()) if orig == typed)
    minutes = elapsed_time / 60
    wpm = (correct_words / minutes) if minutes > 0 else 0
    accuracy = calculate_accuracy(text, user_input)
    return round(wpm), accuracy

def calculate_accuracy(original, typed):
    if len(typed) == 0:
        return 0
    original_words = original.split()
    typed_words = typed.split()
    correct_words = sum(1 for orig, typed in zip(original_words, typed_words) if orig == typed)
    accuracy = (correct_words / len(original_words)) * 100
    return round(accuracy, 2)

def get_test_duration():
    while True:
        duration = input("Enter the test duration in seconds (default is 60): ")
        if duration == "":
            return 60
        if duration.isdigit():
            return int(duration)
        print("Please enter a valid number.")

def timer_thread(duration, stop_event):
    start_time = time.time()
    while not stop_event.is_set() and time.time() - start_time < duration:
        remaining = duration - int(time.time() - start_time)
        sys.stdout.write(f"\033[2A\rTime remaining: {remaining} seconds\033[2B")
        sys.stdout.flush()
        time.sleep(0.1)
    stop_event.set()

def run_single_test(test_duration):
    clear_screen()
    print("Welcome to the WPM Typing Test!")
    print("\nType the following text as quickly and accurately as you can:")
    
    text = get_random_text()
    print(f"\n{text}\n")
    
    input("Press Enter when you're ready to start...")
    clear_screen()
    print(f"Start typing:\n\n{text}\n")
    print("\n\n") # Add two empty lines for the timer and cursor
    
    user_input = []
    stop_event = threading.Event()
    timer = threading.Thread(target=timer_thread, args=(test_duration, stop_event))
    timer.start()
    
    start_time = time.time()
    while not stop_event.is_set():
        if os.name == 'nt':  # Windows-specific input handling
            if msvcrt.kbhit():
                char = msvcrt.getwch()
                if char:
                    user_input.append(char)
                    sys.stdout.write(char)
                    sys.stdout.flush()
    
    elapsed_time = min(time.time() - start_time, test_duration)
    user_input = ''.join(user_input)
    wpm, accuracy = calculate_wpm(text, elapsed_time, user_input)
    
    return wpm, accuracy, elapsed_time

def run_typing_test():
    while True:
        test_duration = get_test_duration()
        wpm, accuracy, elapsed_time = run_single_test(test_duration)
        
        clear_screen()
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        print(f"Your typing speed: {wpm} WPM")
        print(f"Accuracy: {accuracy}%")
        
        restart = input("\nPress 'R' to restart the test or any other key to exit: ")
        if restart.lower() != 'r':
            break

def main():
    run_typing_test()

if __name__ == "__main__":
    main()
