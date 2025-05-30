from cryptography.fernet import Fernet


def decrypt_password(encrypted_password):
    key_file_path = "encryption_key.key"

    with open(key_file_path, "rb") as key_file:
        key = key_file.read()

    cipher_suite = Fernet(key)

    decrypted_password = cipher_suite.decrypt(encrypted_password.encode())
    return decrypted_password.decode()
