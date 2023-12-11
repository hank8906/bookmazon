from enumeration.SystemMessage import CommonSystemCode

class JsonMessage:
    def __init__(self):
        self.success = True
        self.system_code = CommonSystemCode.SUCCESS.value.get('system_code')
        self.system_message = CommonSystemCode.SUCCESS.value.get('message')
        self.data = None
