from odoo import models, fields, api


class IncomingPaymentCallback(models.Model):
    _name = 'radius_manager.incoming_payment_callback'
    _description = 'Incoming Payment Callback'

    data_id = fields.Char(string='Data ID', readonly=True)
    incoming_payment_id = fields.Many2one('radius_manager.incoming_payments',
                                          string='Incoming Payment', readonly=True)
    data_type = fields.Char(string='Data Type', readonly=True)
    initiation_time = fields.Datetime(string='Initiation Time', readonly=True)
    status = fields.Char(string='Status', readonly=True)
    event_type = fields.Char(string='Event Type', readonly=True)
    resource_id = fields.Char(string='Resource ID', readonly=True)
    reference = fields.Char(string='Reference', readonly=True)
    origination_time = fields.Datetime(string='Origination Time', readonly=True)
    sender_phone_number = fields.Char(string='Sender Phone Number', readonly=True)
    amount = fields.Float(string='Amount', readonly=True)
    currency = fields.Char(string='Currency', readonly=True)
    till_number = fields.Char(string='Till Number', readonly=True)
    system = fields.Char(string='System', readonly=True)
    resource_status = fields.Char(string='Resource Status', readonly=True)
    sender_first_name = fields.Char(string='Sender First Name', readonly=True)
    sender_middle_name = fields.Char(string='Sender Middle Name')
    sender_last_name = fields.Char(string='Sender Last Name', readonly=True)
    customer_id = fields.Char(string='Customer ID', readonly=True)
    metadata_reference = fields.Char(string='Metadata Reference', readonly=True)
    notes = fields.Char(string='Notes', readonly=True)
    callback_url = fields.Char(string='Callback URL', readonly=True)
    self_url = fields.Char(string='Self URL', readonly=True)

    @api.model
    def create_from_json(self, data):
        attributes = data.get('data', {}).get('attributes', {})
        event = attributes.get('event', {})
        resource = event.get('resource', {})
        metadata = attributes.get('metadata', {})
        links = attributes.get('_links', {})

        incoming_payment_id = self.env['radius_manager.incoming_payments'].search(
            [('uuid', '=', metadata.get('reference'))])
        if not incoming_payment_id:
            raise ValueError("Incoming Payment not found.")

        vals = {
            'data_id': data.get('data', {}).get('id'),
            'incoming_payment_id': incoming_payment_id.id,
            'data_type': data.get('data', {}).get('type'),
            'initiation_time': attributes.get('initiation_time'),
            'status': attributes.get('status'),
            'event_type': event.get('type'),
            'resource_id': resource.get('id'),
            'reference': resource.get('reference'),
            'origination_time': resource.get('origination_time'),
            'sender_phone_number': resource.get('sender_phone_number'),
            'amount': float(resource.get('amount', 0)),
            'currency': resource.get('currency'),
            'till_number': resource.get('till_number'),
            'system': resource.get('system'),
            'resource_status': resource.get('status'),
            'sender_first_name': resource.get('sender_first_name'),
            'sender_middle_name': resource.get('sender_middle_name'),
            'sender_last_name': resource.get('sender_last_name'),
            'customer_id': metadata.get('customer_id'),
            'metadata_reference': metadata.get('reference'),
            'notes': metadata.get('notes'),
            'callback_url': links.get('callback_url'),
            'self_url': links.get('self')
        }

        return self.create([vals])
