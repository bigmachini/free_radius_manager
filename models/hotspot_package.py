from odoo import models, fields, api
from odoo.exceptions import ValidationError
from .config import host, port, username, password
from ..utils.usermanager_profiles import UserManagerProfiles
import logging

router = UserManagerProfiles(host=host, port=port, username=username, password=password, debug=True)



class HotspotPackage(models.Model):
    _name = 'radius_manager.hotspot_package'
    _description = 'Hotspot Package'

    name = fields.Char(string='Package Name', required=True)
    hotspot_profile_id = fields.Many2one('radius_manager.hotspot_profile', string='Hotspot Profile', required=True)
    hotspot_profile_limitation_id = fields.Many2one('radius_manager.hotspot_profile_limitation',
                                                    string='Hotspot Profile Limitation', required=True)

    def create_hotspot_profile(self):
        """
        Create a new User Manager profile.
        """

        if self.partner_id.kredo_username is None:
            raise ValidationError("Kredoh Username is required to create a user.")

        try:
            router.connect()
            response = router.add_profile(name=self.name, owner=self.partner_id.kredoh_username,
                                          name_for_users=self.display_name, price=self.price,
                                          validity=self.validity)
            logging.info(f"Profile '{response}' created successfully!")
            profile = router.get_profile_by_name(self.name)
            logging.info(f"Profile: {profile}")
            if profile:
                self.hotspot_profile_id = profile.get(".id")
        except Exception as e:
            logging.error(f"Error creating hotspot profile: {e}")
