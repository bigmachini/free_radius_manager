from .mikrotik import MikroTik


class UserManagerProfiles(MikroTik):
    """
    A class to manage User Manager profiles on a MikroTik router.
    Inherits from the MikroTik class.
    """

    def add_profile(
            self,
            name,
            owner,
            name_for_users="",
            price=0,
            validity="1d",
    ):
        """
        Add a new User Manager profile.

        :param name: The name of the User Manager profile.
        :param name_for_users: Name to assign to users under this profile (default: "").
        :param override_shared_users: Number of shared users (e.g., 4 or "off").
        :param owner: Owner of the profile (default: "admin").
        :param price: Price of the profile (default: 0).
        :param starts_at: When the profile starts (e.g., "logon").
        :param validity: Validity of the profile (e.g., "1d").
        :return: The RouterOS response.
        """
        params = {
            "name": name,
            "name-for-users": name_for_users,
            "owner": owner,
            'starts-at': 'logon',
            "price": price,
            "validity": validity,
        }

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/add", params)
        return response



    def update_profile(self, profile_id, **kwargs):
        """
        Update an existing User Manager profile.

        :param profile_id: The unique ID of the profile to update.
        :param kwargs: Key-value pairs of the fields to update.
        :return: The RouterOS response.
        """
        if not profile_id:
            raise ValueError("Profile ID is required to update a profile.")

        # Include the profile ID in the command
        params = {".id": profile_id}
        params.update(kwargs)  # Add all the fields to be updated

        try:
            # Execute the update command
            response = self.execute("/tool/user-manager/profile/set", params)
            return response
        except Exception as e:
            print(f"Error updating profile {profile_id}: {e}")
            return []

    def list_profiles(self):
        """
        List all existing User Manager profiles.

        :return: A list of profiles.
        """
        response = self.execute("/tool/user-manager/profile/print", is_list=True)
        return response

    def get_profile_by_name(self, profile_name):
        """
        Get the profile ID for a specific profile name.

        :param profile_name: The profile name to search for.
        :return: The profile ID, or None if the profile does not exist.
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("name") == profile_name:
                return profile
        return None

    def delete_profile(self, profile_id):
        """
        Delete a User Manager profile.

        :param profile_id: The unique ID of the profile to delete.
        :return: The RouterOS response.
        """
        params = {".id": profile_id}

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/remove", params)
        return response
