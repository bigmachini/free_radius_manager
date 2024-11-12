from odoo import models, fields


class Nas(models.Model):
    _name = 'nas'
    _description = 'Network Access Server'

    nasname = fields.Char(string="NAS Name", required=True, index=True)
    shortname = fields.Char(string="Short Name", required=True)
    type = fields.Char(string="Type", required=True)
    ports = fields.Char(string="Ports", required=True)
    secret = fields.Char(string="Secret", required=True)
    server = fields.Char(string="Server", required=True)
    community = fields.Char(string="Community", required=True)
    description = fields.Text(string="Description")
