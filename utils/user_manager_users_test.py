from user_manager_users import UserManager
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

host = config.get('mikrotik', 'host')
port = config.getint('mikrotik', 'port')
username = config.get('mikrotik', 'username')
password = config.get('mikrotik', 'password')

router = UserManager(host=host, port=port, username=username, password=password, debug=True)

try:
    router.connect()
    print("Connected to MikroTik.")

    response = router.get_user_username(username="test_user_1")
    print(f"Get User Response: {response}")

    if not response:
        response = router.create_user(username="test_user_1", password="password", customer="api")
        print(f"Create User response: {response}")

    response = router.update_user(username="test_user_1", password="newpassword", disabled='true', shared_users=2)
    print(f"Update User Response: {response}")

    response = router.get_user_username(username="test_user_1")
    print(f"Get User Response: {response}")

    response = router.delete_user(username="test_user_1")
    print(f"Get Delete User Response: {response}")

    response = router.get_user_username(username="test_user_1")
    print(f"Get User Response: {response}")

finally:
    router.disconnect()
    print("Disconnected from MikroTik.")
