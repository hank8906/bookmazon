"""
    使用者資訊
"""
class UserBo():
    def __init__(self, user_account, user_name, user_gender, user_password, user_identification, user_email,
                 user_birthday, user_profile_pic):
        self.user_account = user_account
        self.user_name = user_name
        self.user_gender = user_gender
        self.user_password = user_password
        self.user_identification = user_identification
        self.user_email = user_email
        self.user_birthday = user_birthday
        self.user_profile_pic = user_profile_pic

# isolate to communicate service layer abd ORM
