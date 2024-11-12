from odoo import models, fields

class RadCheck(models.Model):
    _name = 'radcheck'
    _description = 'RADIUS Check'

    username = fields.Char(string="Username", required=True, index=True)
    attribute = fields.Char(string="Attribute", required=True)
    op = fields.Char(string="Operator", default=":=", required=True)
    value = fields.Char(string="Value", required=True)