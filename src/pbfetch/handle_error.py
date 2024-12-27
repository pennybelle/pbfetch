def error(traceback, details=None):
    if details:
        return f"Error: {details}: {traceback}"
    else:
        return f"Error: {traceback}"
