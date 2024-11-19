from odoo import models, fields


class STKRequest(models.Model):
    _inherit = 'safaricom_stk.stk_request'

    hotspot_user_id = fields.Many2one('radius_manager.hotspot_user', string='Hotspot User', readonly=True)
    user_profile_limitation_id = fields.Many2one('radius_manager.user_profile_limitation',
                                                 string='User Profile Limitation', readonly=True)
