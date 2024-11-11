import hashlib
import os
import csv

USER_CSV_FILE = 'Lab-8/users.csv'

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if the CSV file exists, and create it if not
def check_csv_file():
    if not os.path.exists(USER_CSV_FILE):
        with open(USER_CSV_FILE, 'w', newline='') as file:
            csv.writer(file).writerow(['username', 'password'])

# Load all users into memory as a dictionary {username: hashed_password}
def load_users():
    check_csv_file()
    with open(USER_CSV_FILE, 'r') as file:
        return {row[0]: row[1] for row in csv.reader(file) if row}

# Save a new user to the CSV file
def save_user(username, hashed_password):
    with open(USER_CSV_FILE, 'a', newline='') as file:
        csv.writer(file).writerow([username, hashed_password])

# Register a new user
def register_user(users):
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists.")
    else:
        save_user(username, hash_password(input("Enter a password: ")))
        print(f"User {username} registered successfully!")

# Log in a user
def login_user(users):
    username = input("Enter your username: ")
    password = hash_password(input("Enter your password: "))
    if users.get(username) == password:
        print(f"Login successful! Welcome, {username}.")
    else:
        print("Invalid username or password.")

# Main user management loop
def user_management():
    users = load_users()  # Load users only once
    while True:
        choice = input("\n1. Sign Up\n2. Login\n3. Exit\nChoose an option: ")
        if choice == '1':
            register_user(users)
            users = load_users()  # Reload users after registration
        elif choice == '2':
            login_user(users)
        elif choice == '3':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    print("Rank Mansi")
    print("22BCP284")

    user_management()