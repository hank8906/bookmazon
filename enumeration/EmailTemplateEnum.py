from enum import Enum

class EmailTemplateEnum(Enum):
    FORGOT_PASSWORD = {'subject': '[Bookmazon.com] 會員忘記密碼驗證', 'file_path': 'login/forgot_password_email.html'}
    RESET_PASSWORD = {'subject': '[Bookmazon.com] 會員密碼變更通知', 'file_path': 'login/reset_password_email.html'}
