from .mikrotik import MikroTik


class HotspotSessionManager(MikroTik):
    """
    A class to manage active hotspot sessions in MikroTik.
    Inherits from the MikroTik class for API interaction.
    """

    def get_active_sessions(self):
        """
        Retrieve all active hotspot sessions.
        :return: A list of dictionaries containing session details.
        """
        try:
            response = self.execute("/tool/user-manager/user/print", is_list=True)
            return response
        except Exception as e:
            print(f"Error retrieving active sessions: {e}")
            return []

    def get_user_sessions(self, username):
        """
        Retrieve active sessions for a specific user.
        :param username: The username to filter sessions.
        :return: A list of dictionaries containing session details for the user.
        """
        try:
            # Get all active sessions
            sessions = self.execute("/tool/user-manager/user/print", is_list=True)

            # Filter sessions for the specified username
            user_sessions = [session for session in sessions if session.get("username") == username]

            if not user_sessions:
                print(f"No active sessions found for user '{username}'.")
            return user_sessions
        except Exception as e:
            print(f"Error retrieving sessions for user {username}: {e}")
            return []

    def disconnect_user(self, username):
        """
        Disconnect all sessions for a specific user.
        :param username: The username of the user to disconnect.
        :return: The MikroTik API response.
        """
        try:
            session_ids = self.execute(f"/ip/hotspot/active/print where username={username}", is_list=True)
            for session in session_ids:
                if ".id" in session:
                    self.execute(f"/ip/hotspot/active/remove=.id={session['.id']}")
            return {"status": "success", "message": f"Disconnected user {username}"}
        except Exception as e:
            print(f"Error disconnecting user {username}: {e}")
            return {"status": "error", "message": str(e)}

        x = [{'.id': '*1', 'customer': 'admin', 'actual-profile': 'unlimited', 'username': 'iphone',
              'password': 'iphone', 'ipv6-dns': '::', 'shared-users': 'unlimited', 'wireless-psk': '',
              'wireless-enc-key': '', 'wireless-enc-algo': 'none', 'uptime-used': '1h35m2s',
              'download-used': '25790850', 'upload-used': '5281690', 'last-seen': 'nov/12/2024 18:18:30',
              'active-sessions': '1', 'active': 'false', 'incomplete': 'false', 'disabled': 'false'},
             {'.id': '*2', 'customer': 'api_user', 'username': '7a:5d:d3:1d:bd:6b',
              'password': '7a:5d:d3:1d:bd:6b', 'ipv6-dns': '::', 'shared-users': '1', 'wireless-psk': '',
              'wireless-enc-key': '', 'wireless-enc-algo': 'none', 'last-seen': 'never', 'active': 'false',
              'incomplete': 'false', 'disabled': 'false'}]
