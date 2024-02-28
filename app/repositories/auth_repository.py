

class AuthRepository():
    def __init__(self):
        self.users = {
            'user1': {'password': 'hashed_password1'},
            'user2': {'password': 'hashed_password2'}
        }

    def user_exists(self, username):
        return username in self.users

    def get_user_password(self, username):
        if self.user_exists(username):
            return self.users[username]['password']
        return None