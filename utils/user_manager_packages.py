from .mikrotik import MikroTik
import logging


class UserManagerPackages(MikroTik):
    def create_package(
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
        logging.info(f"UserManagerPackages::associate_limitation response --> {response}")

        return response

    def list_packages(self):
        """
        List all existing Packages.

        :return: A list of limitations, or an empty list if none exist.
        """
        try:
            # Execute the command to fetch limitations
            response = self.execute("/tool/user-manager/profile/profile-limitation/print", is_list=True)
            logging.info(f"UserManagerPackages::list_packages response --> {response}")
            return response
        except Exception as e:
            logging.error(f"UserManagerPackages::list_packages Exception e -> {e}")
            return []

    def get_package_by_name(self, profile_name, limitation_name):
        """
        Get the user ID for a specific username.

        :param profile_name: Name of the profile.
        :param limitation_name: Name of the limitation.

        :return: None or the Package object.
        """
        profiles = self.list_packages()
        for profile in profiles:
            if profile.get("profile") == profile_name and profile.get("limitation") == limitation_name:
                return profile
        return None

    def update_package(self, package_id, from_time="0s", till_time="23h59m59s", weekdays=None):
        """
        Update an existing Package

        :param package_id: ID for package.
        :param from_time: Start time (default: "0s").
        :param till_time: End time (default: "23h59m59s").
        :param weekdays: Days for the limitation (e.g., "sunday,monday,tuesday").

        :return: The RouterOS response.
        """

        try:
            params = {
                ".id": package_id,
                "from-time": from_time,
                "till-time": till_time,
                "weekdays": weekdays,
            }

            # Execute the command on the router
            response = self.execute("/tool/user-manager/profile/profile-limitation/set", params)
            logging.info(f"UserManagerPackages::update_package response --> {response}")

            return response
        except Exception as e:
            logging.info(f"UserManager::update_package:: Error updating package e --> {e}")
            return []

    def delete_package(self, package_id):
        """
        Delete a Hotspot Package.

        :param package_id: The unique ID of the package.
        :return: The RouterOS response.
        """
        params = {".id": package_id}

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/profile-limitation/remove", params)
        return response
