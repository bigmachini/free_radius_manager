from odoo import models, fields, api


class UserProfileLimitation(models.Model):
    _name = 'radius_manager.user_profile_limitation'
    _description = 'User Profile Limitation'

    name = fields.Char(string="Name", compute='_compute_name', readonly=True)
    hotspot_profile_limitation_id = fields.Many2one('radius_manager.hotspot_profile_limitation',
                                                    string="Hotspot Profile Limitation", readonly=True)
    hotspot_user_id = fields.Many2one('radius_manager.hotspot_user', string="Hotspot User", readonly=True)
    download_speed = fields.Char(related='hotspot_profile_limitation_id.hotspot_limitation_id.rate_limit_rx',)
    upload_speed = fields.Char(related='hotspot_profile_limitation_id.hotspot_limitation_id.rate_limit_tx',)
    validity = fields.Char(related='hotspot_profile_limitation_id.hotspot_profile_id.validity', )
    is_activated = fields.Boolean(string="Is Activated", default=False)

    @api.depends('hotspot_user_id.name', 'hotspot_profile_limitation_id.name')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.hotspot_user_id.name} - {record.hotspot_profile_limitation_id.name}'
