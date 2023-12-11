class BusinessError(Exception):
    def __init__(self, message, error_code):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message
        self.error_code = error_code
