from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    kredoh_username = fields.Char(string="Kredoh Username", required=[('is_kredoh_partner', '=', True)])
    is_kredoh_partner = fields.Boolean(string="Is Kredoh Partner")
    unique_code = fields.Char(string="Unique Code", required=[('is_kredoh_partner', '=', True)])
    hotspot_user_ids = fields.One2many('radius_manager.hotspot_user', 'res_partner_id', string="Hotspot Users")
    hotspot_user_count = fields.Integer(string="Hotspot Users Count", compute='_compute_hotspot_user_count')

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if 'unique_code' in vals:
            unique_code = vals['unique_code']
            if len(unique_code) != 4:
                raise ValidationError("Unique Code must be exactly 4 characters long.")
        return res

    def _compute_hotspot_user_count(self):
        for record in self:
            record.hotspot_user_count = len(record.hotspot_user_ids)
