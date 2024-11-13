import logging

from odoo import models, fields, api

from ..utils.user_manager_sessions import HotspotSessionManager
from .config import host, port, username, password

router = HotspotSessionManager(host=host, port=port, username=username, password=password, debug=True)


class HotspotUserSession(models.Model):
    _name = 'radius_manager.hotspot_user_session'
    _description = 'User Sessions'

    customer = fields.Char(string='Customer', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    hotspot_user = fields.Char(string='Username', required=True)
    hotspot_user_id = fields.Many2one('radius_manager.hotspot_user', string='Hotspot User', required=True)
    calling_station_id = fields.Char(string='MAC Address', required=True)
    acct_session_id = fields.Char(string='Session ID', required=True)
    user_ip = fields.Char(string='User IP', required=True)
    host_ip = fields.Char(string='Host IP', required=True)
    status = fields.Char(string='Status', required=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    terminate_cause = fields.Char(string='Terminate Cause', required=True)
    uptime = fields.Char(string='Uptime', required=True)
    download = fields.Char(string='Download', required=True)
    upload = fields.Char(string='Upload', required=True)

    @staticmethod
    def get_sessions():
        """
        Get all user sessions from the User Manager.
        """
        sessions = router.get_active_sessions()
        logging.info(f"HotspotUserSession::get_sessions Sessions:{sessions}")
