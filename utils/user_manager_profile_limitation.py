from .mikrotik import MikroTik
import logging


class UserManagerProfileLimitation(MikroTik):
    def create_profile_limitation(
            self, profile_name, limitation_name, from_time="0s", till_time="23h59m59s", weekdays=None
    ):
        """
        Associate a limitation with a User Manager profile.

        :param profile_name: Name of the profile.
        :param limitation_name: Name of the limitation.
        :param from_time: Start time (default: "0s").
        :param till_time: End time (default: "23h59m59s").
        :param weekdays: Days for the limitation (e.g., "sunday,monday,tuesday").
        :return: The RouterOS response.
        """
        if not weekdays:
            weekdays = "sunday,monday,tuesday,wednesday,thursday,friday,saturday"

        params = {
            "profile": profile_name,
            "limitation": limitation_name,
            "from-time": from_time,
            "till-time": till_time,
            "weekdays": weekdays,
        }

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/profile-limitation/add", params)
        logging.info(f"UserManagerProfileLimitation::associate_limitation response --> {response}")

        return response

    def list_profile_limitation(self):
        """
        List all existing profile_limitation.

        :return: A list of limitations, or an empty list if none exist.
        """
        try:
            # Execute the command to fetch limitations
            response = self.execute("/tool/user-manager/profile/profile-limitation/print", is_list=True)
            logging.info(f"UserManagerProfileLimitation::list_profile_limitation response --> {response}")
            return response
        except Exception as e:
            logging.error(f"UserManagerProfileLimitation::list_profile_limitation Exception e -> {e}")
            return []

    def get_profile_limitation_by_name(self, profile_name, limitation_name, profile_limitation_id=None):
        """
        Get the user ID for a specific username.

        :param profile_name: Name of the profile.
        :param limitation_name: Name of the limitation.

        :return: None or the profile_limitation object.
        """
        profiles = self.list_profile_limitation()
        for profile in profiles:
            if (profile.get("profile") == profile_name and profile.get("limitation") == limitation_name) or (
                    profile.get(".id") == profile_limitation_id):
                return profile
        return None

    def get_profile_limitation_by_id(self, profile_limitation_id):
        """
        Get the user ID for a specific username.

        :param profile_limitation_id: ID of profile limitation.

        :return: None or the profile_limitation object.
        """
        profiles = self.list_profile_limitation()
        for profile in profiles:
            if profile.get(".id") == profile_limitation_id:
                return profile
        return None

    def update_profile_limitation(self, profile_limitation_id, from_time="0s", till_time="23h59m59s", weekdays=None):
        """
        Update an existing profile_limitation

        :param profile_limitation_id: ID for profile_limitation.
        :param from_time: Start time (default: "0s").
        :param till_time: End time (default: "23h59m59s").
        :param weekdays: Days for the limitation (e.g., "sunday,monday,tuesday").

        :return: The RouterOS response.
        """

        try:
            params = {
                ".id": profile_limitation_id,
                "from-time": from_time,
                "till-time": till_time,
                "weekdays": weekdays,
            }

            # Execute the command on the router
            response = self.execute("/tool/user-manager/profile/profile-limitation/set", params)
            logging.info(f"UserManagerProfileLimitation::update_profile_limitation response --> {response}")

            return response
        except Exception as e:
            logging.info(f"UserManager::update_profile_limitation:: Error updating profile_limitation e --> {e}")
            return []

    def delete_profile_limitation(self, profile_limitation_id):
        """
        Delete a Hotspot profile_limitation.

        :param profile_limitation_id: The unique ID of the profile_limitation.
        :return: The RouterOS response.
        """
        params = {".id": profile_limitation_id}

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/profile-limitation/remove", params)
        return response
