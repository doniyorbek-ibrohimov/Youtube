import time
import asyncio

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
     

#Version 1 - blocking
def fetch_user_sync(user_id: int) -> str:
    time.sleep(2)  # Simulate a delay in fetching user data
    return f"User {user_id}"

#Version 2 - non-blocking
async def fetch_user_async(user_id: int) -> str:
    await asyncio.sleep(2)  # Simulate a delay in fetching user data
    return f"User {user_id}"
     

if __name__ == "__main__":
    # Syncm - fetch 3 users, measure time
    start_time = time.time()
    for i in range(1, 4):
        print(fetch_user_sync(i))
    print(f"Time taken for synchronous fetching: {time.time() - start_time:.2f} seconds") # 6 seconds 

    # Async - fetch 3 users, measure time
    async def main():
        start_time = time.time()
        results = await asyncio.gather(
            fetch_user_async(1),
            fetch_user_async(2),
            fetch_user_async(3))
        print(results)
        # for i in range(1, 4):
        #     print(await fetch_user_async(i))
        print(f"Time taken for asynchronous fetching: {time.time() - start_time:.2f} seconds") # 2 seconds
    asyncio.run(main())
