#!/usr/bin/env python3
import random
import string
import json
from crypto_tools import md5_hash, base64_decode, generate_jwt_token
from colorama import init, Fore, Back, Style

def generate_password(length=12, uppercase=True, lowercase=True, numbers=True, special_characters=True):
    characters = ''
    
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if numbers:
        characters += string.digits
    if special_characters:
        characters += string.punctuation

    if not characters:
        raise ValueError("at least one character set (uppercase, lowercase, numbers, special characters) must be selected.")

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def usernames_from_file(filename):
    try:
        with open(filename, 'r') as file:
            usernames = [line.strip() for line in file.readlines()]
        return usernames
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []

def generate_bulk_passwords(usernames, length=12, uppercase=True, lowercase=True, numbers=True, special_characters=True):
    passwords = {}
    
    for username in usernames:
        try:
            password = generate_password(length, uppercase, lowercase, numbers, special_characters)
            passwords[username] = password
        except ValueError as e:
            passwords[username] = str(e)

    return passwords

def gen_single_password(username, length=12, uppercase=True, lowercase=True, numbers=True, special_characters=True):
    try:
        password = generate_password(length, uppercase, lowercase, numbers, special_characters)
        return {username: password}
    except ValueError as e:
        return {username: str(e)}

def save_to_file(filename, content):
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Passwords saved to '{filename}' successfully.")
    except Exception as e:
        print(f"Error saving to file: {str(e)}")

def menu():
    print("""
🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
🟥🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
🟥🟥🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛
🟥🟥🟥🟥⬜⬜⬜⬜⬜⬜⬜⬜⬜
🟥🟥🟥🟥🟥⬜⬜⬜⬜⬜⬜⬜⬜
🟥🟥🟥🟥⬜⬜⬜⬜⬜⬜⬜⬜⬜
🟥🟥🟥🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
🟥🟥🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩
🟥🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩 ® Free Palestine
██╗      █████╗  ██████╗ ███████╗███╗   ██╗
██║     ██╔══██╗██╔════╝ ██╔════╝████╗  ██║
██║     ███████║██║  ███╗█████╗  ██╔██╗ ██║
██║     ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║
███████╗██║  ██║╚██████╔╝███████╗██║ ╚████║
╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═══╝
    """)
    print("1. Single password with username")
    print("2. Bulk passwords with usernames")
    print("3. Password only")
    print("4. Bulk passwords only")
    print("5. MD5 Hash")
    print("6. Base64 decode")
    print("7. Generate JWT token")
    print("0. Exit")

def main():
    while True:
        menu()
        option = input("Choose (0-7): ")

        if option == '0':
            print("Exit. LOLbye!")
            break

        elif option == '1':
            username = input("Username: ")
            length = int(input("Password length: "))
            uppercase = input("Uppercase letters? (y/n): ").lower() == 'y'
            lowercase = input("Lowercase letters? (y/n): ").lower() == 'y'
            numbers = input("Include numbers? (y/n): ").lower() == 'y'
            special_characters = input("Special characters? (y/n): ").lower() == 'y'

            result = gen_single_password(username, length, uppercase, lowercase, numbers, special_characters)
            print("\nPassword: ")
            for username, password in result.items():
                print(f"{username}: {password}")

            save_option = input("Save the password to file? (y/n): ").lower()
            if save_option == 'y':
                filename = input("Filename to be saved as: ")
                save_to_file(filename, f"{username}: {password}")

        elif option == '2':
            source_option = input("Method (1: Manual Entry, 2: File 'usernames.txt'): ")
            
            if source_option == '1':
                usernames_str = input("Comma-separated list of usernames (e.g., user1,user2): ")
                usernames = [username.strip() for username in usernames_str.split(',')]
            elif source_option == '2':
                usernames = usernames_from_file('usernames.txt')
            else:
                print("source option invalid . choose 1 or 2.")
                continue

            length = int(input("Password length: "))
            uppercase = input("Uppercase letters? (y/n): ").lower() == 'y'
            lowercase = input("Lowercase letters? (y/n): ").lower() == 'y'
            numbers = input("Include numbers? (y/n): ").lower() == 'n'
            special_characters = input("Include special characters? (y/n): ").lower() == 'y'

            bulk_passwords = generate_bulk_passwords(usernames, length, uppercase, lowercase, numbers, special_characters)
            print("\nPasswords: ")
            for username, password in bulk_passwords.items():
                print(f"{username}: {password}")

            save_option = input("Save the passwords to a file? (y/n): ").lower()
            if save_option == 'y':
                filename = input("Filename to be saved as: ")
                save_to_file(filename, "\n".join([f"{username}: {password}" for username, password in bulk_passwords.items()]))

        elif option == '3':
            length = int(input("Password length: "))
            uppercase = input("Uppercase letters? (y/n): ").lower() == 'y'
            lowercase = input("Lowercase letters? (y/n): ").lower() == 'y'
            numbers = input("Include numbers? (y/n): ").lower() == 'y'
            special_characters = input("Include special characters? (y/n): ").lower() == 'y'

            try:
                password = generate_password(length, uppercase, lowercase, numbers, special_characters)
                print("\nPassword:  ", password)
            except ValueError as e:
                print("\nError:", e)

        elif option == '4':
            num_passwords = int(input("Enter total passwords to generate in bulk: "))
            length = int(input("Password length: "))
            uppercase = input("Uppercase letters? (y/n): ").lower() == 'y'
            lowercase = input("Lowercase letters? (y/n): ").lower() == 'y'
            numbers = input("Include numbers? (y/n): ").lower() == 'y'
            special_characters = input("Include special characters? (y/n): ").lower() == 'y'

            bulk_passwords = generate_bulk_passwords(list(range(1, num_passwords + 1)), length, uppercase, lowercase, numbers, special_characters)
            print("\nPasswords: ")
            for username, password in bulk_passwords.items():
                print(f"{username}: {password}")

            save_option = input("Save the passwords to a file? (y/n): ").lower()
            if save_option == 'y':
                filename = input("Enter the filename: ")
                save_to_file(filename, "\n".join([f"{username}: {password}" for username, password in bulk_passwords.items()]))

        elif option == '5':
            data = input("Enter data for MD5 hashing: ")
            hashed_data = md5_hash(data)
            print("\nMD5 Hash:", hashed_data)

        elif option == '6':
            data = input("Enter data for Base64 decoding: ")
            decoded_data = base64_decode(data)
            print("\nBase64 Decoded:", decoded_data)

        elif option == '7':
            try:
                with open('payload.json', 'r') as file:
                    payload_str = file.read()
                    payload = json.loads(payload_str)
            except FileNotFoundError:
                print("Error: Payload file 'payload.json' not found.")
                continue
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in 'payload.json'.")
                continue

            secret_key = input("Enter secret key for JWT token: ")
            
            print("Choose the signing algorithm:")
            print("1. HS256 (HMAC using SHA-256)")
            print("2. HS384 (HMAC using SHA-384)")
            print("3. HS512 (HMAC using SHA-512)")
            algorithm_choice = input("Choose desired algorithm: ")
            
            algorithms_mapping = {
                '1': 'HS256',
                '2': 'HS384',
                '3': 'HS512',

            }
            
            selected_algorithm = algorithms_mapping.get(algorithm_choice)
            
            if selected_algorithm is None:
                print("algorithm choice Invalid . Exiting.")
                continue
            
            jwt_token = generate_jwt_token(payload, secret_key, algorithm=selected_algorithm)
            print("\nGenerated JWT Token:", jwt_token)

        else:
            print("Invalid option. Choose a number between 0 and 7.")
        continue_option = input("Exit Or Continue? (y/n):  ").lower()
        if continue_option != 'y':
            break

if __name__ == "__main__":
    main()
