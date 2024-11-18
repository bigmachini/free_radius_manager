import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from .config import host, port, username, password
from ..utils.user_manager_users import UserManager

USER_MANAGER_PATH = "/tool/user-manager/user"

router = UserManager(host=host, port=port, username=username, password=password, debug=True)


class HotspotUser(models.Model):
    _name = 'radius_manager.hotspot_user'
    _description = 'Customer'

    name = fields.Char(string="Name", required=True)
    username = fields.Char(string="Username", readonly=True)
    password = fields.Char(string="password", readonly=True)
    phone = fields.Char(string="Phone")
    partner_id = fields.Many2one('res.partner', string='Partner', required=True,
                                 domain=[('is_kredoh_partner', '=', True)])
    hotspot_user_id = fields.Char(string="Hotspot User ID", readonly=True)
    disabled = fields.Boolean(string="Disabled", default=False)
    user_profile_limitation_ids = fields.One2many('radius_manager.user_profile_limitation', 'hotspot_user_id',
                                                  string="User Profile Limitations")
    hotspot_user_session_ids = fields.One2many('radius_manager.hotspot_user_session', 'hotspot_user_id',
                                               string="User Sessions")

    def cron_check_and_deactivate_profile_limitation(self):
        users_with_profiles = self.search([('user_profile_limitation_ids', '!=', False)])
        for user in users_with_profiles:
            user.check_and_deactivate_profile_limitation()

    def check_and_deactivate_profile_limitation(self):
        logging.info(f"HotspotUser::check_and_deactivate_profile_limitation")

        active_user_profile_limitation = self.user_profile_limitation_ids.filtered(lambda p: p.is_activated)
        if not active_user_profile_limitation:
            logging.info("No active profile limitation found.")
            return

        hotspot_profile_limitation = active_user_profile_limitation.hotspot_profile_limitation_id
        hotspot_limitation = hotspot_profile_limitation.hotspot_limitation_id
        uptime_limit = hotspot_limitation.uptime_limit

        latest_session = self.hotspot_user_session_ids.sorted(key=lambda s: s.create_date, reverse=True)[:1]
        if not latest_session:
            logging.info("No sessions found.")
            return

        latest_session_uptime = latest_session.uptime
        if latest_session_uptime == uptime_limit:
            active_user_profile_limitation.is_activated = False
            logging.info("Profile limitation deactivated due to matching uptime.")

    def create_hotspot_user(self):
        """
        Create a new User Manager user.
        """
        logging.info(f"HotspotUser::create_hotspot_user")

        if self.partner_id.kredoh_username is None:
            raise ValidationError("Kredoh Username is required to create a user.")

        try:
            router.connect()
            response = router.create_user(username=self.username, customer=self.partner_id.kredoh_username)
            if len(response) == 2:
                error_msg = response[0]['']
                raise ValidationError(f"Failed to create user: {error_msg}")

            logging.info(f"User '{response}' created successfully!")
            user = router.get_user_by_identifier(self.username)
            logging.info(f"User: {user}")
            if user:
                self.hotspot_user_id = user.get(".id")
                logging.info(f"User ID: {self.hotspot_user_id}")

        finally:
            router.disconnect()
            logging.info("HotspotUser::create_hotspot_user Disconnected from MikroTik.")

    def disable_hotspot_user(self):
        logging.info(f"HotspotUser::disable_user")

        try:
            router.connect()
            response = router.update_user(user_id=self.hotspot_user_id, username=self.username, password=self.password,
                                          disabled=True,
                                          customer=self.partner_id.kredoh_username)
            if len(response) == 2:
                error_msg = response[0]['']
                raise ValidationError(f"Failed to disable user: {error_msg}")

            logging.info(f"HotspotUser::disable_userUser '{response}' disabled successfully!")
            self.disabled = True

        finally:
            router.disconnect()
            logging.info("HotspotUser::disable_userUser Disconnected from MikroTik.")

    def enable_hotspot_user(self):
        logging.info(f"HotspotUser::enable_hotspot_user")

        try:
            router.connect()
            response = router.update_user(user_id=self.hotspot_user_id, username=self.username, password=self.password,
                                          disabled=False,
                                          customer=self.partner_id.kredoh_username)
            if len(response) == 2:
                error_msg = response[0]['']
                raise ValidationError(f"Failed to enable user: {error_msg}")

            logging.info(f"HotspotUser::enable_hotspot_user '{response}' disabled successfully!")
            self.disabled = False

        finally:
            router.disconnect()
            logging.info("HotspotUser::disable_userUser Disconnected from MikroTik.")

    def assign_profile_user(self, profile_name):
        self.ensure_one()
        logging.info(f"HotspotUser::assign_profile_user")

        try:
            router.connect()
            user = router.get_user_by_identifier(self.username)
            if user:
                response = router.assign_profile_to_user(customer=self.partner_id.kredoh_username,
                                                         number=user.get("number"),
                                                         profile_name=profile_name)
                if len(response) == 2:
                    error_msg = response[0]['']
                    raise ValidationError(f"Failed to ASSIGN profile to user: {error_msg}")
                logging.info(f"HotspotUser::assign_profile_user '{response}' assigned successfully!")

        finally:
            router.disconnect()
            logging.info("HotspotUser::assign_profile_user Disconnected from MikroTik.")
