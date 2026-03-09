username = input("Enter your username: ")


def validate_username(username):
    if len(username) < 3:
        print("Username must be at least 3 characters long.")
        return False
    

print(username.isalnum)