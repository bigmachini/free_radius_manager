from datetime import datetime


def bytes_to_human_readable(byte_count):
    """
    Convert bytes to a human-readable string format (GB, MB, KB).
    """
    byte_count = float(byte_count)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_count < 1024:
            return f"{byte_count:.2f} {unit}"
        byte_count /= 1024


def convert_to_odoo_timestamp(date_str):
    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_str, "%b/%d/%Y %H:%M:%S")
    # Format the datetime object to a string compatible with Odoo
    odoo_timestamp = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return odoo_timestamp
