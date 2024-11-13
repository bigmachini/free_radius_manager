import logging
import os

from odoo import models, fields, api
from odoo.orm.decorators import readonly
from ..utils.user_manager_users import UserManager

USER_MANAGER_PATH = "/tool/user-manager/user"
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Specify the full path to the config.ini file
config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')

# Read the config file
config.read(config_file_path)

host = config.get('mikrotik', 'host')
port = config.getint('mikrotik', 'port')
username = config.get('mikrotik', 'username')
password = config.get('mikrotik', 'password')

router = UserManager(host=host, port=port, username=username, password=password, debug=True)


class HotspotUser(models.Model):
    _name = 'radius_manager.hotspot_user'
    _description = 'Customer'

    name = fields.Char(string="Name", required=True)
    username = fields.Char(string="Username", readonly=True)
    password = fields.Integer(string="password", readonly=True)
    phone = fields.Char(string="Phone")
    res_partner_id = fields.Many2one('res.partner', string="Partner", domain=[('is_kredoh_partner', '=', True)],
                                     required=True, readonly=True)
    hotspot_user_id = fields.Char(string="Hotspot User ID", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            code = vals["phone"][-6:]
            partner = self.env['res.partner'].browse(vals["res_partner_id"])
            vals["username"] = f'{partner.unique_code.upper()}_{code}'
            vals["password"] = code
        return super(HotspotUser, self).create(vals_list)

    def create_hotspot_user(self):
        """
        Create a new User Manager user.
        """

        try:
            router.connect()
            response = router.create_user(username=self.username, password=self.password, customer="fran_beauty")
            logging.info(f"User '{response}' created successfully!")
            user = router.get_user_username(username=self.username)
            logging.info(f"User: {user}")
            if user:
                self.hotspot_user_id = user.get(".id")
                logging.info(f"User ID: {self.hotspot_user_id}")

        except Exception as e:
            print(f"Failed to create user: {e}")
        finally:
            router.disconnect()
            logging.info("Disconnected from MikroTik.")
