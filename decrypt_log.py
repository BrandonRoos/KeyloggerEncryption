from cryptography.fernet import Fernet

LOG_FILE = "keyfile_encrypted.txt"
KEY_FILE = "encryption_key.key"

# Load the encryption key
with open(KEY_FILE, 'rb') as key_file:
    key = key_file.read()

cipher = Fernet(key)

# Decrypt the log file
with open(LOG_FILE, 'rb') as encrypted_log:
    for line in encrypted_log:
        try:
            print(cipher.decrypt(line).decode().strip())
        except Exception as e:
            print(f"Decryption error: {e}")