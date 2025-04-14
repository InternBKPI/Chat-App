from pynput import keyboard
from pynput.keyboard import Controller, Key
import time
import threading

FORBIDDEN_WORDS = ["badword", "secret"]
typed_chars = []
keyboard_controller = Controller()

listener = None  # global reference to the listener
processing = False

def replace_forbidden_words(text):
    for word in FORBIDDEN_WORDS:
        text = text.replace(word, "-" * len(word))
    return text

def on_press(key):
    global typed_chars, processing, listener

    if processing:
        return  # ignore keys during processing

    try:
        if key == Key.enter:
            processing = True

            typed_text = ''.join(typed_chars)
            print(f"[DEBUG] Original: {typed_text}")

            filtered_text = replace_forbidden_words(typed_text)
            print(f"[DEBUG] Filtered: {filtered_text}")

            # Stop listener to prevent loop
            listener.stop()
            time.sleep(0.1)

            # Simulate filtered input (new line + filtered)
            keyboard_controller.press(Key.enter)
            keyboard_controller.release(Key.enter)
            time.sleep(0.05)

            for char in filtered_text:
                keyboard_controller.type(char)
                time.sleep(0.005)

            keyboard_controller.press(Key.enter)
            keyboard_controller.release(Key.enter)

            typed_chars = []
            processing = False

            # Restart listener
            start_listener()

        elif key == Key.space:
            typed_chars.append(' ')
        elif key == Key.backspace:
            if typed_chars:
                typed_chars.pop()
        elif hasattr(key, 'char') and key.char is not None:
            typed_chars.append(key.char)

    except Exception as e:
        print(f"[ERROR] {e}")
        processing = False
        start_listener()

def start_listener():
    global listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

def main():
    print("Censorship keylogger running. Press Ctrl+C to stop.")
    start_listener()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by user.")

if __name__ == "__main__":
    main()
