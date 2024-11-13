from odoo import models,fields

class Router(models.Model):
    _name = 'radius_manager.router'
    _description = 'Router'

    name = fields.Char(string="Name", required=True)