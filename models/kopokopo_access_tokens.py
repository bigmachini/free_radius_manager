from odoo import models, fields, api


class KopokopoAccessTokens(models.Model):
    _name = 'radius_manager.kopokopo_access_tokens'
    _description = 'Kopokopo Access Tokens'

    access_token = fields.Char(string='Access Token', readonly=True)
    token_type = fields.Char(string='Token Type', readonly=True)
    expires_in = fields.Integer(string='Expires In', readonly=True)
    created_at = fields.Datetime(string='Created At', readonly=True)
    kopo_kopo_id = fields.Many2one('radius_manager.kopokopo', string='Kopo Kopo', readonly=True)
