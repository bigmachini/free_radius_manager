import re


def validate_mac_address(mac):
    # validate MAC address
    mac_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return mac_pattern.match(mac)
