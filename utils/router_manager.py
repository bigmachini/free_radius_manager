import logging

from .mikrotik import MikroTik


class RouterManager(MikroTik):
    def get_router_info(self):
        """
        Get Router Info.
        """
        try:
            self.connect()
            response = self.execute("/system/resource/print",  is_list=True)
            return response
        finally:
            self.disconnect()
