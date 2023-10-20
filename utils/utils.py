from typing import Union

def get_response_dict( message: str, data : Union[list, dict] = None, error_details=None) -> dict:
    """
    Returns a dictionary with the given message and data
    """
    return {
        "message": message,
        "data": data,
        "error_details": error_details
    }