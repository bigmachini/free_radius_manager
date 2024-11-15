import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from .config import host, port, username, password
from ..utils.user_manager_profiles import UserManagerProfiles

router = UserManagerProfiles(host=host, port=port, username=username, password=password, debug=True)


class HotspotProfile(models.Model):
    _name = 'radius_manager.hotspot_profile'
    _description = 'Hotspot Profile'

    name = fields.Char(string='Profile Name', required=True)
    name_for_user = fields.Char(string='User Display Name', required=True,
                                help='The name to display on the hotspot login page.')
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 domain=[('is_kredoh_partner', '=', True)])
    validity = fields.Char(string='Validity', required=True,
                           help='The validity of the profile in seconds(s),minutes(m),hours(h),days(d) or unlimited')
    price = fields.Float(string='Price', required=True)
    hotspot_profile_id = fields.Char(string="Hotspot Profile ID", readonly=True)

    def create_hotspot_profile(self):
        """
        Create a new User Manager profile.
        """

        if self.partner_id.kredoh_username is None:
            raise ValidationError("Kredoh Username is required to create a user.")

        try:
            router.connect()
            response = router.add_profile(name=self.name, owner=self.partner_id.kredoh_username,
                                          name_for_users=self.display_name, price=self.price,
                                          validity=self.validity)
            if len(response) == 2:
                error_msg = response[0]['']
                raise ValidationError(f"Failed to create profile: {error_msg}")

            logging.info(f"Profile '{response}' created successfully!")
            profile = router.get_profile_by_name(self.name)
            logging.info(f"Profile: {profile}")
            if profile:
                self.hotspot_profile_id = profile.get(".id")
        except Exception as e:
            logging.error(f"HotspotProfile::update_hotspot_profile Error creating hotspot profile e --> {e}")
        finally:
            router.disconnect()

    def update_hotspot_profile(self):
        """
        Update an existing Hotspot Profile.
        """
        try:
            router.connect()
            response = router.update_profile(profile_id=self.hotspot_profile_id, name=self.name,
                                             owner=self.partner_id.kredoh_username,
                                             name_for_users=self.display_name, price=self.price,
                                             validity=self.validity)
            if len(response) == 2:
                error_msg = response[0]['']
                raise ValidationError(f"Failed to update profile: {error_msg}")

            logging.info(f"HotspotProfile::update_hotspot_profile response {response}")
        except Exception as e:
            logging.error(f"HotspotProfile::update_hotspot_profile  Error creating hotspot profile  e --> {e}")
        finally:
            router.disconnect()

    def delete_hotspot_profile(self):
        """
        Delete an existing Hotspot profile.
        """
        try:
            router.connect()
            response = router.delete_profile(self.hotspot_profile_id)

            if len(response) == 2:
                error_msg = response[0]['']
                raise ValidationError(f"Failed to delete profile: {error_msg}")

            self.hotspot_profile_id = None
            logging.info(f"HotspotProfile::delete_profile  response {response}!")
        except Exception as e:
            logging.error(f"HotspotProfile::delete_profile Exception e -->{e}")
        finally:
            router.disconnect()
