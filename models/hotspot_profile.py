from odoo import models, fields, api

class HotspotProfile(models.Model):
    _name = 'radius_manager.hotspot_profile'
    _description = 'Hotspot Profile'

    name = fields.Char(string='Profile Name', required=True)
    display_name = fields.Char(string='Display Name', required=True, help='The name to display on the hotspot login page.')
    res_partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    validity = fields.Char(string='Validity', required=True, help='The validity of the profile in Mins,Hour,Day,Month,Year.')
    price = fields.Float(string='Price', required=True)

    @api.model
    def create(self, vals):
        res = super(HotspotProfile, self).create(vals)
        return res

    def write(self, vals):
        res = super(HotspotProfile, self).write(vals)
        return res