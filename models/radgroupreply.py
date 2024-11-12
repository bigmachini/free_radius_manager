from odoo import models, fields

class RadGroupReply(models.Model):
    _name = 'radgroupreply'
    _description = 'RADIUS Group Reply'

    groupname = fields.Char(string="Group Name", required=True, index=True)
    attribute = fields.Char(string="Attribute", required=True)
    op = fields.Char(string="Operator", default=":=", required=True)
    value = fields.Char(string="Value", required=True)