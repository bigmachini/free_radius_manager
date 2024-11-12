from odoo import models, fields

class RadUserGroup(models.Model):
    _name = 'radusergroup'
    _description = 'RADIUS User Group'

    username = fields.Char(string="Username", required=True, index=True)
    groupname = fields.Char(string="Group Name", required=True)
    priority = fields.Integer(string="Priority", default=1)