from .mikrotik import MikroTik
import logging

class UserManager(MikroTik):
    """
    A class to manage users in MikroTik User Manager.
    Inherits from the MikroTik class.
    """

    """
    customer=api 
    username="testing" 
    password="testing" 
    disabled=false
    shared-users=4
    """

    def create_user(self, username, password, customer, shared_users=None):
        """
        Create a new user in User Manager.

        :param username: Username for the new user.
        :param password: Password for the new user.
        :param customer: customer of the user (default: "admin").
        :param shared_users: Number of shared users (default: None).
        :return: The RouterOS response.
        """
        if not username:
            raise ValueError("Username is required to create a user.")
        if not password:
            raise ValueError("Password is required to create a user.")
        if not customer:
            raise ValueError("Customer is required to create a user.")

        params = {
            "username": username,
            "password": password,
            "customer": customer,
        }
        if shared_users:
            params["shared-users"] = shared_users

        try:
            response = self.execute("/tool/user-manager/user/add", params)
            return response
        except Exception as e:
            logging.info(f"Error creating user {username}: {e}")
            return []

    def get_user_username(self, username):
        """
        Get the user ID for a specific username.

        :param username: The username to search for.
        :return: The user ID, or None if the user does not exist.
        """
        users = self.list_users()
        for user in users:
            if user.get("username") == username:
                return {
                    ".id": user.get(".id"),
                    "username": user.get("username"),
                    "password": user.get("password"),
                    "customer": user.get("customer"),
                    "disabled": user.get("disabled"),
                }
        return None

    def update_user(self, username, **kwargs):
        """
        Update an existing user's details.

        :param username: Username of the user to update.
        :param kwargs: Key-value pairs of the fields to update.
        :return: The RouterOS response.
        """
        # Find the user ID based on the username
        user = self.get_user_username(username)
        if not user:
            raise ValueError(f"User {username} does not exist.")

        if 'shared_users' in kwargs:
            user['shared-users'] = kwargs.pop('shared_users')
        user.update(kwargs)

        try:
            logging.info('user', user)
            response = self.execute("/tool/user-manager/user/set", user)
            return response
        except Exception as e:
            logging.info(f"UserManager::update_user:: Error updating user {username}: {e}")
            return []

    def list_users(self):
        """
        List all users in User Manager.

        :return: A list of users.
        """
        try:
            response = self.execute("/tool/user-manager/user/print", is_list=True)
            return response
        except Exception as e:
            logging.info(f"Error listing users: {e}")
            return []

    def delete_user(self, username):
        """
        Delete a user from User Manager.

        :param username: Username of the user to delete.
        :return: The RouterOS response.
        """
        # Find the user ID based on the username
        user = self.get_user_username(username)
        if not user:
            raise ValueError(f"User {username} does not exist.")

        try:
            params = {".id": user.get(".id")}
            response = self.execute("/tool/user-manager/user/remove", params)
            return response
        except Exception as e:
            logging.info(f"Error deleting user {username}: {e}")
            return []

    def assign_user_to_group(self, username, group):
        """
        Assign a user to a specific group.

        :param username: Username of the user.
        :param group: Group to assign the user to.
        :return: The RouterOS response.
        """
        # Find the user ID based on the username
        user_id = self.get_user_id(username)
        if not user_id:
            raise ValueError(f"User {username} does not exist.")

        params = {
            ".id": user_id,
            "group": group,
        }

        try:
            response = self.execute("/tool/user-manager/user/set", params)
            return response
        except Exception as e:
            logging.info(f"Error assigning user {username} to group {group}: {e}")
            return []

    def list_profiles(self):
        """
        List all profiles in User Manager.

        :return: A list of profiles.
        """
        try:
            response = self.execute("/tool/user-manager/profile/logging.info")
            return response
        except Exception as e:
            logging.info(f"Error listing profiles: {e}")
            return []

    def validate_profile(self, profile_name):
        """
        Validate if a profile exists in User Manager.

        :param profile_name: The name of the profile to validate.
        :return: True if the profile exists, False otherwise.
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("name") == profile_name:
                return True
        return False

    def get_profile_id(self, profile_name):
        """
        Get the profile ID for a specific profile name.

        :param profile_name: The profile name to search for.
        :return: The profile ID, or None if the profile does not exist.
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("name") == profile_name:
                return profile.get(".id")
        return None

    def assign_profile_to_user(self, username, profile_name):
        """
        Assign a User Manager profile to a user.

        :param username: Username of the user.
        :param profile_name: Name of the profile to assign.
        :return: The RouterOS response.
        """
        user_id = self.get_user_id(username)
        if not user_id:
            raise ValueError(f"User {username} does not exist.")

        profile_id = self.get_profile_id(profile_name)
        if not profile_id:
            raise ValueError(f"Profile {profile_name} does not exist.")

        params = {
            ".id": user_id,
            "profile": profile_name
        }

        try:
            response = self.execute("/tool/user-manager/user/set", params)
            return response
        except Exception as e:
            logging.info(f"Error assigning profile {profile_name} to user {username}: {e}")
            return []

    def activate_user_profile(self, username, profile_name):
        """
        Activate a profile assigned to a user.

        :param username: The username of the user.
        :param profile_name: The profile to activate for the user.
        :return: The RouterOS response.
        """
        # Get user ID
        user_id = self.get_user_id(username)
        if not user_id:
            raise ValueError(f"User {username} does not exist.")

        # Get profile ID
        profile_id = self.get_profile_id(profile_name)
        if not profile_id:
            raise ValueError(f"Profile {profile_name} does not exist.")

        # Activate the profile
        params = {
            "user": user_id,
            "profile": profile_name,
        }

        try:
            response = self.execute("/tool/user-manager/user/activate", params)
            return response
        except Exception as e:
            logging.info(f"Error activating profile {profile_name} for user {username}: {e}")
            return []
