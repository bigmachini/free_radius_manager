import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

# Specify the full path to the config.ini file
config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')

# Read the config file
config.read(config_file_path)

host = config.get('mikrotik', 'host')
port = config.getint('mikrotik', 'port')
username = config.get('mikrotik', 'username')
password = config.get('mikrotik', 'password')
