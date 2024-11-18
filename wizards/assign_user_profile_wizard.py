from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging


class AssignUserProfileWizard(models.TransientModel):
    _name = 'radius_manager.assign_user_profile_wizard'
    _description = 'Assign User to Profile Wizard'

    hotspot_user_id = fields.Many2one('radius_manager.hotspot_user', string='Hotspot User', required=True,
                                      readonly=True)
    hotspot_profile_limitation_id = fields.Many2one('radius_manager.hotspot_profile_limitation',
                                                    string='Hotspot Profile Limitation', required=True)
    activate_profile = fields.Boolean(string="Activate Profile", default=False)

    @api.model
    def default_get(self, default_fields):
        res = super(AssignUserProfileWizard, self).default_get(default_fields)
        if self.env.context.get('default_hotspot_user_id'):
            res['hotspot_user_id'] = self.env.context['default_hotspot_user_id']
        return res

    def assign_profile(self):
        self.ensure_one()

        if not self.hotspot_user_id or not self.hotspot_profile_limitation_id:
            raise ValidationError("Both Hotspot User and Hotspot Profile Limitation are required.")

        if not self.hotspot_profile_limitation_id.hotspot_profile_limitation_id:
            raise ValidationError("Profile Limitation not created.")

        if not self.hotspot_user_id.hotspot_user_id:
            raise ValidationError("User not created.")

        profile = self.env['radius_manager.user_profile_limitation'].search(
            [('hotspot_user_id', '=', self.hotspot_user_id.id),
             ('hotspot_profile_limitation_id', '=', self.hotspot_profile_limitation_id.id),
             ('is_activated', '=', True)], limit=1)

        if profile:
            raise ValidationError(f"Profile already assigned")

        user_profile_limitation = self.env['radius_manager.user_profile_limitation'].create([{
            'hotspot_user_id': self.hotspot_user_id.id,
            'hotspot_profile_limitation_id': self.hotspot_profile_limitation_id.id,
            'partner_id': self.hotspot_user_id.partner_id.id,
            'is_activated': True
        }])

        if user_profile_limitation:
            self.hotspot_user_id.assign_profile_user(self.hotspot_profile_limitation_id.hotspot_profile_id.name)
