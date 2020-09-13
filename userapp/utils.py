def get_serializer_error(e):
    """

    :return:
    """

    try:
        error_message = e.args if not isinstance(e.args, tuple) and not isinstance(e.args, list) else e.args[0]
        if isinstance(error_message, list):
            if len(error_message) > 1 and not error_message[0]:
                error_message = error_message[1]
            else:
                error_message = error_message[0]
        if isinstance(error_message, dict):
            error = list(error_message.values())[0]
            if isinstance(error, list):
                error_message = error[0]
            else:
                error_message = error
    except Exception:
        error_message = 'Please check the values'

    return error_message