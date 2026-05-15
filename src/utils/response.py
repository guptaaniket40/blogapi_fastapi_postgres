def success_response(message: str, data=None):
    return {
        "message": message,
        "data": data
    }


def error_response(message: str):
    return {
        "message": message
    }