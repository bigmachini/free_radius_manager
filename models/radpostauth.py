from odoo import models, fields

class RadPostAuth(models.Model):
    _name = 'radpostauth'
    _description = 'RADIUS Post Auth'

    username = fields.Char(string="Username", required=True, index=True)
    password = fields.Char(string="Password", required=True)
    reply = fields.Char(string="Reply", required=True)
    authdate = fields.Datetime(string="Auth Date", required=True)