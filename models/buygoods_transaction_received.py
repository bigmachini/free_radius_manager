from odoo import models, fields, api


class BuygoodsTransactionReceived(models.Model):
    _name = 'radius_manager.buygoods_transaction_received'
    _description = 'Buygoods Transaction Received'

    topic = fields.Char(string='Topic', readonly=True)
    transaction_id = fields.Char(string='Transaction ID', readonly=True)
    created_at = fields.Datetime(string='Created At', readonly=True)
    event_type = fields.Char(string='Event Type', readonly=True)
    resource_id = fields.Char(string='Resource ID', readonly=True)
    amount = fields.Float(string='Amount', readonly=True)
    status = fields.Char(string='Status', readonly=True)
    system = fields.Char(string='System', readonly=True)
    currency = fields.Char(string='Currency', readonly=True)
    reference = fields.Char(string='Reference', readonly=True)
    till_number = fields.Char(string='Till Number', readonly=True)
    sender_phone_number = fields.Char(string='Sender Phone Number', readonly=True)
    hashed_sender_phone = fields.Char(string='Hashed Sender Phone', readonly=True)
    origination_time = fields.Datetime(string='Origination Time', readonly=True)
    sender_last_name = fields.Char(string='Sender Last Name', readonly=True)
    sender_first_name = fields.Char(string='Sender First Name', readonly=True)
    sender_middle_name = fields.Char(string='Sender Middle Name')
    self_link = fields.Char(string='Self Link', readonly=True)
    resource_link = fields.Char(string='Resource Link', readonly=True)
    kopokopo_webhook_id = fields.Many2one('radius_manager.kopokopo_webhook', string='Webhook ID', readonly=True)
    kopokopo_id = fields.Many2one('radius_manager.kopokopo', string='Kopo Kopo', readonly=True)

