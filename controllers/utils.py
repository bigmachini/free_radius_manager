import logging
import re
import phonenumbers


def validate_mac_address(mac):
    # validate MAC address
    mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return mac_pattern.match(mac)


def validate_and_format_phone_number(phone_number, region='KE'):
    try:
        parsed_number = phonenumbers.parse(phone_number, region)
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164).replace('+', '')
        else:
            logging.error(f"validate_and_format_phone_number:: Invalid phone number: {phone_number}")
            return None
    except phonenumbers.NumberParseException as e:
        logging.error(f"validate_and_format_phone_number:: Error parsing phone number: {e}")
        return None
