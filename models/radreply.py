from odoo import models, fields


class RadReply(models.Model):
    _name = 'radreply'
    _description = 'RADIUS Reply'

    username = fields.Char(string="Username", required=True, index=True)
    attribute = fields.Char(string="Attribute", store=True, readonly=True)
    op = fields.Char(string="Operator", default=":=", required=True)
    value = fields.Char(string="Value", required=True)
