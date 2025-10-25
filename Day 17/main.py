class User:
    # ...
    # pass
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.followers = 0
        self.following = 0

    def follow(self, user):
        print(f"{self.username} has followed {user.username}")
        user.followers += 1
        self.following += 1


user_1 = User("001", "Alessandro")
user_2 = User("002", "Anna")
print(f"{user_2.username} followers = {user_2.followers}")
user_1.follow(user_2)
print(f"{user_2.username} followers = {user_2.followers}")
# user_1.id ="001"
# user_1.username ="Myself"
# print(user_1.username)