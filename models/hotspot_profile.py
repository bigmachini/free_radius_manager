from odoo import models, fields, api
from .config import host, port, username, password
from ..utils.usermanager_profiles import UserManagerProfiles
import logging

router = UserManagerProfiles(host=host, port=port, username=username, password=password, debug=True)


class HotspotProfile(models.Model):
    _name = 'radius_manager.hotspot_profile'
    _description = 'Hotspot Profile'

    name = fields.Char(string='Profile Name', required=True)
    name_for_name = fields.Char(string='Display Name', required=True,
                               help='The name to display on the hotspot login page.')
    res_partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    validity = fields.Char(string='Validity', required=True,
                           help='The validity of the profile in seconds(s),minutes(m),hours(h),days(d) or unlimited')
    price = fields.Float(string='Price', required=True)
    hotspot_profile_id = fields.Char(string="Hotspot Profile ID", readonly=True)

    def create_hotspot_profile(self):
        """
        Create a new User Manager profile.
        """
        try:
            router.connect()
            response = router.add_profile(name=self.name, name_for_users=self.display_name, price=self.price,
                                          validity=self.validity)
            logging.info(f"Profile '{response}' created successfully!")
            profile = router.get_profile_by_name(self.name)
            logging.info(f"Profile: {profile}")
            if profile:
                self.hotspot_profile_id = profile.get(".id")
        except Exception as e:
            logging.error(f"Error creating hotspot profile: {e}")

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HotspotProfile, self).create(vals_list)
        return res

    def write(self, vals):
        res = super(HotspotProfile, self).write(vals)
        return res
