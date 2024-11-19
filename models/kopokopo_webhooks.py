from odoo import models, fields, api
import requests
import hmac
import hashlib

EVENT_TYPES = [('buygoods_transaction_received', 'Buygoods Transaction Received'),
               ('buygoods_transaction_reversed', 'Buygoods Transaction Reversed'),
               ('b2b_transaction_received', 'B2B Transaction Received'),
               ('m2m_transaction_received', 'M2M Transaction Received'),
               ('settlement_transfer_completed', 'Settlement Transfer Completed'),
               ('customer_created', 'Customer Created')]
SCOPE = [('till', 'Till Number'),
         ('company', 'Company'),
         ]


class KopokopoWebhook(models.Model):
    _name = 'radius_manager.kopokopo_webhook'
    _description = 'Kopokopo Webhook'

    event_type = fields.Selection(EVENT_TYPES, string='Event Type', required=True)
    webhook_url = fields.Char(string='Webhook URL', required=True)
    scope = fields.Selection(SCOPE, string='Scope', required=True)
    scope_value = fields.Char(string='Scope Value')
    kopo_kopo_id = fields.Many2one('radius_manager.kopokopo', string='Kopo Kopo', required=True)
    active = fields.Boolean(string='Active', default=True)
    buygoods_transaction_received_ids = fields.One2many('radius_manager.buygoods_transaction_received',
                                                        'kopokopo_webhook_id', string='Buygoods Transaction Received')

    def create_webhook(self, vals):
        kopo_kopo = self.env['radius_manager.kopokopo'].browse(int(vals.get('kopo_kopo_id')))
        if not kopo_kopo:
            raise ValueError("Kopo Kopo not found.")
        url = kopo_kopo.webhook_subscription_url

        access_token = kopo_kopo.get_access_token().get('access_token', None)
        if not access_token:
            raise ValueError("Access Token not found.")

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
        payload = {
            "event_type": vals.get('event_type'),
            "url": vals.get('webhook_url'),
            "scope": vals.get('scope'),
            "scope_reference": vals.get('scope_value')
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def validate_kopokopo_webhook(request_body, kopokopo_signature, api_key):
        """
        Validate the Kopo Kopo webhook signature.

        :param request_body: The raw request body from the webhook.
        :param kopokopo_signature: The value of the X-KopoKopo-Signature header.
        :param api_key: Your Kopo Kopo API key.
        :return: True if the signature is valid, False otherwise.
        """
        # Compute the HMAC SHA256 hash of the request body using the API key
        computed_signature = hmac.new(
            key=api_key.encode('utf-8'),
            msg=request_body,
            digestmod=hashlib.sha256
        ).hexdigest()

        # Compare the computed signature with the provided signature
        return hmac.compare_digest(computed_signature, kopokopo_signature)
