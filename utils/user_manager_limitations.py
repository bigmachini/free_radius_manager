import logging

from .mikrotik import MikroTik


class UserManagerLimitations(MikroTik):
    def add_limitation(
            self,
            name,
            owner,
            rate_limit_rx=None,
            rate_limit_tx=None,
            rate_limit_min_rx=None,
            rate_limit_min_tx=None,
            transfer_limit=None,
            uptime_limit="60m",
    ):
        """
        Add a limitation Profile.
        :param name: Name of the limitation.
        :param owner: One of the profile.
        :param rate_limit_rx: Download speed (e.g., "1M").
        :param rate_limit_tx: Upload speed (e.g., "1M").
        :param rate_limit_min_rx: Download speed (e.g., "1M").
        :param rate_limit_min_tx: Upload speed (e.g., "1M").
        :param transfer_limit: Data transfer limit (e.g., "1000B").
        :param uptime_limit: Maximum uptime (default: "0s").
        :return: The RouterOS response.
        """

        params = {"name": name,
                  "owner": owner,
                  # "rate-limit-burst-limit-rx": 0,
                  # "rate-limit-burst-limit-tx": 0,
                  # "burst-threshold-rx": 0,
                  # "burst-threshold-tx": 0,
                   "rate-limit-burst-time-rx": '5s',
                   "rate-limit-burst-time-tx": '5s'
                  }
        if rate_limit_rx:
            params["rate-limit-rx"] = rate_limit_rx.upper()
        if rate_limit_tx:
            params["rate-limit-tx"] = rate_limit_tx.upper()
        if rate_limit_min_rx:
            params["rate-limit-min-rx"] = rate_limit_min_rx.upper()
        if rate_limit_min_tx:
            params["rate-limit-min-tx"] = rate_limit_min_tx.upper()
        if transfer_limit:
            params["transfer-limit"] = transfer_limit.upper()

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/limitation/add", params)
        return response

    def get_limitation_by_identifier(self, profile_id=None, profile_name=None):
        """
        Get Limitation by Profile Name.

        :param profile_name: The username to search for.
        :param profile_id: ID of the profile.
        :return: The user ID, or None if the user does not exist.
        """
        profiles = self.list_limitations()
        for profile in profiles:
            if profile.get("name") == profile_name or profile.get(".id") == profile_id:
                return {
                    ".id": profile.get(".id"),
                    "name": profile.get("name"),
                    "owner": profile.get("owner"),
                    "rate-limit-rx": profile.get("rate-limit-rx"),
                    "rate-limit-tx": profile.get("rate-limit-tx"),
                    "transfer-limit": profile.get("transfer-limit"),

                }
        return None

    def update_limitation(self, limitation_id, name, owner, rate_limit_rx, rate_limit_tx, rate_limit_min_rx,
                          rate_limit_min_tx, transfer_limit,
                          uptime_limit="60m",
                          ):
        """
        Update a limitation Profile.
        :param limitation_id: ID of limitation to update.
        :param name: Name of the limitation.
        :param owner: One of the profile.
        :param rate_limit_rx: Download speed (e.g., "1M").
        :param rate_limit_tx: Upload speed (e.g., "1M").
        :param rate_limit_min_rx: Download Min speed (e.g., "1M").
        :param rate_limit_min_tx: Upload Min speed (e.g., "1M").
        :param transfer_limit: Data transfer limit (e.g., "1000B").
        :param uptime_limit: Maximum uptime (default: "0s").
        :return: The RouterOS response.
        """
        params = {".id": limitation_id,
                  "name": name,
                  "owner": owner,
                  "rate-limit-rx": rate_limit_rx.upper(),
                  "rate-limit-tx": rate_limit_tx.upper(),
                  "rate-limit-min-rx": rate_limit_min_rx.upper(),
                  "rate-limit-min-tx": rate_limit_min_tx.upper(),
                  "transfer-limit": transfer_limit.upper(),
                  "rate-limit-burst-time-rx": '5s',
                  "rate-limit-burst-time-tx": '5s'

                  }

        # Execute the command on the router
        response = self.execute("/tool/user-manager/profile/limitation/set", params)
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
