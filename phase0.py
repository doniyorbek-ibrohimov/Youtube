
class User:
     def __init__(self, username: str, email: str, bio: str = ""):
        self.username = username
        self.email = email
        self.bio = bio
        self.is_email_verified = False

     def __str__(self):
        return self.username
     
     def verify_email(self):
         if all(c.isalnum() or c in "_@." for c in self.email) and "@" in self.email:
             self.is_email_verified = True
             return True, "Email is valid and verified."
         return False
     
     @staticmethod
     def validate_username(username: str) -> tuple[bool, str]:
        if len(username) < 8:
            return False, "Username must be at least 8 characters long."
        if len(username) > 30:
            return False, "Username must be at most 30 characters long."
        if not all(n.isalnum() or n == "_" for n in username):
            return False, "Username can only contain letters, numbers and underscores."
        return True, "Username is valid."
     

if __name__ == "__main__":
    user = User("test_user", "test_user@example.com")
    print(user.validate_username(user.username))
    print(user.verify_email())