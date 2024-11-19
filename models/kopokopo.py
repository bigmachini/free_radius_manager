from odoo import models, fields, api
import requests
from datetime import datetime, timedelta


class Kopokopo(models.Model):
    _name = 'radius_manager.kopokopo'
    _description = 'Kopokopo'

    client_id = fields.Char(string='Client ID', required=True)
    client_secret = fields.Char(string='Client Secret', required=True)
    base_url = fields.Char(string='Base URL', required=True)
    access_token_ids = fields.One2many('radius_manager.kopokopo_access_tokens', 'kopo_kopo_id',
                                       string="Access Tokens")

    def get_access_token(self):
        latest_token = self.access_token_ids.sorted(key=lambda t: t.created_at, reverse=True)[:1]
        if latest_token:
            token = latest_token[0]
            expiry_time = token.created_at + timedelta(seconds=token.expires_in)
            if expiry_time > datetime.now():
                return {
                    "access_token": token.access_token
                }

        response = requests.post(
            f"{self.base_url}/oauth/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            token_data = response.json()
            new_token = self.env['radius_manager.kopokopo_access_tokens'].create({
                "access_token": token_data["access_token"],
                "token_type": token_data["token_type"],
                "expires_in": token_data["expires_in"],
                "created_at": datetime.fromtimestamp(token_data["created_at"]),
                "kopo_kopo_id": self.id
            })
            return {
                "access_token": new_token.access_token,
            }
        else:
            response.raise_for_status()
