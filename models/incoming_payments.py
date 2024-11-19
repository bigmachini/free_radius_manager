import uuid
from email.policy import default

import requests

from odoo import models, fields, api

PAYMENT_STATUS = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed')
]


class IncomingPayments(models.Model):
    _name = 'radius_manager.incoming_payments'
    _description = 'Incoming Payments'

    user_profile_limitation_id = fields.Many2one('radius_manager.user_profile_limitation',
                                                 string='User Profile Limitation', readonly=True)
    amount = fields.Float(string='Amount', readonly=True)
    hotspot_user_id = fields.Many2one('radius_manager.hotspot_user', string='Hotspot User', readonly=True)
    uuid = fields.Char(string='UUID', readonly=True, default=lambda self: str(uuid.uuid4()))
    payment_status = fields.Selection(PAYMENT_STATUS, string='Payment Status', readonly=True)
    kopokopo_id = fields.Many2one('radius_manager.kopokopo', string='Kopokopo', readonly=True)
    incoming_payment_callback_ids = fields.One2many('radius_manager.incoming_payment_callback', 'incoming_payment_id',
                                                    string='Incoming Payment Callbacks')

    def create_incoming_payment(self, phone_number):
        self.ensure_one()
        access_token = self.kopokopo_id.get_access_token()
        url = "https://sandbox.kopokopo.com/api/v1/incoming_payments"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        payload = {
            "payment_channel": "M-PESA STK Push",
            "till_number": self.kopokopo_id.till_number,
            "subscriber": {
                "first_name": "",
                "last_name": "",
                "phone_number": phone_number,
                "email": ""
            },
            "amount": {
                "currency": "KES",
                "value": self.user_profile_limitation_id.hotspot_profile_id.price
            },
            "metadata": {
                "customer_id": str(self.hotspot_user_id.id),
                "reference": self.uuid,
                "notes": f"Payment for {self.user_profile_limitation_id.name}"
            },
            "_links": {
                "callback_url": self.kopokopo_id.incoming_payments_callback_url
            }
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        if response.status_code == 201:
            self.payment_status = 'pending'
        else:
            self.payment_status = 'failed'
        return response.json()
