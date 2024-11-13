from .mikrotik import MikroTik
import logging


class UserManagerLimitations(MikroTik):
    def add_limitation(
            self,
            name,
            owner,
            rate_limit_rx=None,
            rate_limit_tx=None,
            transfer_limit=None,
            uptime_limit="60m",
    ):
        """
        Add a new User Manager profile limitation.

        :param name: Name of the limitation.
        :param rate_limit_rx: Download speed (e.g., "1M").
        :param rate_limit_tx: Upload speed (e.g., "1M").
        :param rate_limit_burst_rx: Burst download speed (e.g., "2M").
        :param rate_limit_burst_tx: Burst upload speed (e.g., "2M").
        :param rate_limit_min_rx: Minimum download speed (e.g., "512k").
        :param rate_limit_min_tx: Minimum upload speed (e.g., "512k").
        :param transfer_limit: Data transfer limit (e.g., "1000B").
        :param upload_limit: Upload limit (e.g., "1000B").
        :param download_limit: Download limit (e.g., "1000B").
        :param uptime_limit: Maximum uptime (default: "0s").
        :return: The RouterOS response.
        """
        params = {"name": name, "uptime-limit": uptime_limit, "owner": owner}
        if rate_limit_rx:
            params["rate-limit-rx"] = rate_limit_rx
        if rate_limit_tx:
            params["rate-limit-tx"] = rate_limit_tx
        if transfer_limit:
            params["transfer-limit"] = transfer_limit

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/limitation/add", params)
        return response

    def get_limitation_by_name(self, profile_name):
        """
        Get the user ID for a specific username.

        :param username: The username to search for.
        :return: The user ID, or None if the user does not exist.
        """
        profiles = self.list_limitations()
        for profile in profiles:
            if profile.get("name") == profile_name:
                return {
                    ".id": profile.get(".id"),
                    "name": profile.get("name"),
                    "uptime-limit": profile.get("uptime-limit"),
                    "owner": profile.get("owner"),
                    "rate-limit-rx": profile.get("rate-limit-rx"),
                    "rate-limit-tx": profile.get("rate-limit-tx"),
                    "transfer-limit": profile.get("transfer-limit"),
                }
        return None

    def update_limitation(self, limitation_id, **kwargs):
        """
        Update an existing User Manager limitation.

        :param limitation_id: The unique ID of the limitation to update.
        :param kwargs: Key-value pairs of the fields to update.
        :return: The RouterOS response.
        """
        if not limitation_id:
            raise ValueError("Limitation ID is required to update a limitation.")

        # Include the limitation ID in the command
        params = {".id": limitation_id}
        params.update(kwargs)  # Add all the fields to be updated

        try:
            # Execute the update command
            response = self.execute("/tool/user-manager/profile/limitation/set", params)
            return response
        except Exception as e:
            print(f"Error updating limitation {limitation_id}: {e}")
            return []

    def associate_limitation(
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
        return response

    def list_limitations(self):
        """
        List all existing User Manager limitations.

        :return: A list of limitations, or an empty list if none exist.
        """
        try:
            # Execute the command to fetch limitations
            response = self.execute("/tool/user-manager/profile/limitation/print", is_list=True)
            logging.info("::list_limitations Raw Response --> {response}")
            return response
        except Exception as e:
            logging.error(f"Error listing limitations: {e}")
            return []

    def delete_limitation(self, limitation_id):
        """
        Delete a User Manager limitation.

        :param limitation_id: The unique ID of the limitation to delete.
        :return: The RouterOS response.
        """
        params = {".id": limitation_id}

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/limitation/remove", params)
        return response
