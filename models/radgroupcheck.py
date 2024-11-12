from odoo import models, fields

class RadGroupCheck(models.Model):
    _name = 'radgroupcheck'
    _description = 'RADIUS Group Check'

    groupname = fields.Char(string="Group Name", required=True, index=True)
    attribute = fields.Char(string="Attribute", required=True)
    op = fields.Char(string="Operator", default=":=", required=True)
    value = fields.Char(string="Value", required=True)