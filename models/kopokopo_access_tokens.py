from odoo import models, fields, api


class KopokopoAccessTokens(models.Model):
    _name = 'radius_manager.kopokopo_access_tokens'
    _description = 'Kopokopo Access Tokens'

    access_token = fields.Char(string='Access Token', required=True)
    token_type = fields.Char(string='Token Type', required=True)
    expires_in = fields.Integer(string='Expires In', required=True)
    created_at = fields.Datetime(string='Created At', required=True)
    kopo_kopo_id = fields.Many2one('radius_manager.kopokopo', string='Kopo Kopo', required=True)
