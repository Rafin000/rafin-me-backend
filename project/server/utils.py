def error_response(status_code, message=None, data=None):
    """
    Generates a standardized error response for API endpoints.

    Args:
        status_code (int): HTTP status code indicating the type of error.
        message (str, optional): Custom error message. If not provided, a default message based on the status code will be used.
        data (dict, optional): Additional data related to the error. If it contains an error message under the key `data["error"]["message"]`, this message will be used.

    Returns:
        tuple: A tuple containing a dictionary with the error response and the HTTP status code.

    The dictionary has the following structure:
        - 'status': A string indicating the failure and the status code.
        - 'message': The error message, either custom or default based on the status code.
        - 'data': Additional data related to the error. This will be shown, if provided.

    Example:
        >>> error_response(404)
        ({'status': 'failed with code 404', 'message': 'Item not found'}, 404)

        >>> error_response(401, message="Custom Unauthorized Message")
        ({'status': 'failed with code 401', 'message': 'Custom Unauthorized Message'}, 401)

        >>> error_response(400, data={"error": {"message": "Invalid input data"}})
        ({'status': 'failed with code 400', 'message': 'Invalid input data', 'data': {"error": {"message": "Invalid input data"}}}, 400)

    """

    status_messages = {
        400: ["Bad Request", "Please provide valid data"],
        401: ["Unauthorized", "Unauthorized token"],
        402: ["Payment Required", "Payment required"],
        403: ["Forbidden", "No token or API key found"],
        404: ["Item Not Found", "Item not found"],
        405: ["Method Not Allowed", "Specified method is invalid for this resource"],
        406: ["Not Acceptable", "URI not available in preferred format"],
        407: ["Proxy Authentication Required", "You must authenticate with this proxy before proceeding"],
        408: ["Request Timeout", "Request timed out; try again later"],
        409: ["Conflict", "Duplicate data found"],
    }

    default_status = "failed with unknown status code"
    default_message = "Unknown Error"

    if data and data["error"]["message"] is not None:
        message = data["error"]["message"]

    status, default_message = status_messages.get(status_code, [default_status, default_message])

    response_object = {
        'status': f'failed with code {status_code}',
        'message': message if message is not None else default_message
    }

    if data is not None:
        response_object["data"]= data
        
    return response_object, status_code