import struct


def _parse_response_list(response):
    """
    Parse the MikroTik response into a structured format.

    :param response: List of strings from the MikroTik response.
    :return: Parsed response as a list of dictionaries.
    """
    parsed_response = []
    current_item = {}

    for line in response:
        # Start a new item when encountering '!re'
        if line == "!re":
            if current_item:  # Save the previous item before starting a new one
                parsed_response.append(current_item)
                current_item = {}
        elif line.startswith("="):  # Process key-value pairs
            key, value = line[1:].split("=", 1)  # Remove the leading '=' and split
            current_item[key] = value
        elif line == "!done":  # End of response
            if current_item:  # Add the last item if it exists
                parsed_response.append(current_item)

    return parsed_response


def _parse_response(response):
    """
    Parse the response into a structured format.

    :param response: List of dictionaries from the MikroTik response.
    :return: Parsed response as a list of dictionaries.
    """
    if not isinstance(response, list):
        raise ValueError("Expected response to be a list.")

    parsed_response = []
    current = {}

    for item in response:
        # If it's a dictionary, no further parsing is needed
        if isinstance(item, dict):
            parsed_response.append(item)
        elif isinstance(item, str):
            if item.startswith("!"):
                if current:
                    parsed_response.append(current)
                current = {"!status": item}
            elif "=" in item:
                key, value = item.split("=", 1)
                current[key] = value

    if current:
        parsed_response.append(current)

    return parsed_response


def encode_length(length):
    """Encode the length of a message."""
    if length < 0x80:
        return struct.pack("!B", length)
    elif length < 0x4000:
        length |= 0x8000
        return struct.pack("!BB", (length >> 8) & 0xFF, length & 0xFF)
    elif length < 0x200000:
        length |= 0xC00000
        return struct.pack("!BBB", (length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF)
    elif length < 0x10000000:
        length |= 0xE0000000
        return struct.pack("!BBBB", (length >> 24) & 0xFF, (length >> 16) & 0xFF, (length >> 8) & 0xFF,
                           length & 0xFF)
    else:
        return struct.pack("!B", 0xF0) + struct.pack("!BBBB", (length >> 24) & 0xFF, (length >> 16) & 0xFF,
                                                     (length >> 8) & 0xFF, length & 0xFF)
