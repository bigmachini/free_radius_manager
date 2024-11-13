
import hashlib
import logging
import socket
import struct
import time

from .utils import encode_length, _parse_response_list, _parse_response


class MikroTik:
    def __init__(self, host, username, password, port, ssl=False, debug=False, timeout=3, attempts=5, delay=3):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ssl = ssl
        self.debug = debug
        self.timeout = timeout
        self.attempts = attempts
        self.delay = delay
        self.connected = False
        self.socket = None

    def log_debug(self, message):
        """Log debug messages."""
        if self.debug:
            logging.info(message)

    def connect(self):
        """Connect to the MikroTik router."""
        for attempt in range(self.attempts):
            try:
                self.log_debug(f"Connection attempt #{attempt + 1} to {self.host}:{self.port}...")
                self.socket = socket.create_connection((self.host, self.port), timeout=self.timeout)
                self.log_debug("Connection established.")
                self.authenticate()
                self.connected = True
                return True
            except Exception as e:
                self.log_debug(f"Connection failed: {e}")
                time.sleep(self.delay)
        raise Exception("Failed to connect after multiple attempts.")

    def disconnect(self):
        """Disconnect from the MikroTik router."""
        if self.socket:
            self.socket.close()
        self.connected = False
        self.log_debug("Disconnected.")

    def authenticate(self):
        """Authenticate with the MikroTik router."""
        # Send /login
        self.write("/login")
        response = self.read()

        # Pre-6.43: Challenge-response authentication
        if len(response) > 1 and "ret" in response[1]:
            challenge = bytes.fromhex(response[1]["ret"])
            md5 = hashlib.md5()
            md5.update(b"\x00" + self.password.encode("utf-8") + challenge)
            hashed_password = md5.hexdigest()
            self.write("/login", {"name": self.username, "response": "00" + hashed_password})
        else:
            # Post-6.43: Simple username/password authentication
            self.write("/login", {"name": self.username, "password": self.password})

        response = self.read()
        if "!done" not in [item.get("!status", "!") for item in response]:
            raise Exception("Authentication failed.")

    def write(self, command, attributes=None):
        """Send a command to the router."""
        if not self.socket:
            raise Exception("Not connected to the router.")

        # Send the command
        self._write_to_socket(command)

        # Send additional attributes if provided
        if attributes:
            for key, value in attributes.items():
                attribute = f"={key}={value}"
                self._write_to_socket(attribute)

        # End the command sequence
        self._write_to_socket("")

    def _write_to_socket(self, data):
        """Send raw data to the socket."""
        encoded_length = encode_length(len(data))
        self.socket.sendall(encoded_length + data.encode("utf-8"))
        self.log_debug(f"<<< {data}")

    def read(self, is_list=False):
        """Read the response from the router."""
        response = []
        while True:
            length = self._read_length()
            if (response and response[-1] == '!done') or (length == 0 and response[-1] == '!done'):
                break
            data = self.socket.recv(length).decode("utf-8")
            response.append(data)
            self.log_debug(f">>> {data}")

        if is_list:
            return _parse_response_list(response)
        else:
            return _parse_response(response)

    def _read_length(self):
        """Read the length of the next message."""
        first_byte = ord(self.socket.recv(1))
        if first_byte & 0x80 == 0x00:
            return first_byte
        elif first_byte & 0xC0 == 0x80:
            second_byte = ord(self.socket.recv(1))
            return ((first_byte & ~0xC0) << 8) + second_byte
        elif first_byte & 0xE0 == 0xC0:
            second_byte, third_byte = self.socket.recv(2)
            return ((first_byte & ~0xE0) << 16) + (second_byte << 8) + third_byte
        elif first_byte & 0xF0 == 0xE0:
            second_byte, third_byte, fourth_byte = self.socket.recv(3)
            return ((first_byte & ~0xF0) << 24) + (second_byte << 16) + (third_byte << 8) + fourth_byte
        elif first_byte == 0xF0:
            return struct.unpack("!I", self.socket.recv(4))[0]

    def execute(self, command, params=None, is_list=False):
        """Execute a command on the router."""
        self.write(command, params)
        return self.read(is_list)
