from flask_login import UserMixin

from model.User import User

class AuthUser(UserMixin):
    def __init__(self, user: User):
        self.user = user

    # login manager
    def get_id(self):
        return self.user.user_account
