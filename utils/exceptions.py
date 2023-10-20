class ConditionFailedException(Exception):
    def __init__(self, message, error_details=None):
        self.message = message
        self.error_details = error_details

    def __str__(self):
        return repr(self.message)
