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
    partner_id = fields.Many2one('res.partner', string="Partner", domain=[('is_kredoh_partner', '=', True)],
                                 required=True)
    hotspot_user_id = fields.Char(string="Hotspot User ID", readonly=True)
    disabled = fields.Boolean(string="Disabled", default=False)
    user_profile_limitation_ids = fields.One2many('radius_manager.user_profile_limitation', 'hotspot_user_id',
                                                  string="User Profile Limitations")
    hotspot_user_session_ids = fields.One2many('radius_manager.hotspot_user_session', 'hotspot_user_id',
                                               string="User Sessions")
    router_id = fields.Many2one('radius_manager.hotspot_router', string='Router', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            code = vals["phone"][-6:]
            partner = self.env['res.partner'].browse(vals["partner_id"])
            vals["username"] = f'{partner.unique_code.lower()}{code}'
            vals["password"] = vals["phone"][-4:]
        return super(HotspotUser, self).create(vals_list)

    def create_hotspot_user(self):
        """
        Create a new User Manager user.
        """
        logging.info(f"HotspotUser::create_hotspot_user")

        if self.partner_id.kredoh_username is None:
            raise ValidationError("Kredoh Username is required to create a user.")

        try:
            router.connect()
            response = router.create_user(username=self.username, password=self.password,
                                          customer=self.partner_id.kredoh_username)
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
