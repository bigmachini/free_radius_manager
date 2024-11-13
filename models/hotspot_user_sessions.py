import logging
import hashlib
from idlelib.pyparse import trans

from reportlab.graphics.transform import transformPoint

from odoo import models, fields, api

from ..utils.user_manager_sessions import HotspotSessionManager
from .config import host, port, username, password

router = HotspotSessionManager(host=host, port=port, username=username, password=password, debug=True)

from datetime import datetime


def convert_to_odoo_timestamp(date_str):
    # Parse the date string to a datetime object
    date_obj = datetime.strptime(date_str, "%b/%d/%Y %H:%M:%S")
    # Format the datetime object to a string compatible with Odoo
    odoo_timestamp = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return odoo_timestamp


def bytes_to_human_readable(byte_count):
    """
    Convert bytes to a human-readable string format (GB, MB, KB).
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if byte_count < 1024:
            return f"{byte_count:.2f} {unit}"
        byte_count /= 1024


class HotspotUserSession(models.Model):
    _name = 'radius_manager.hotspot_user_session'
    _description = 'User Sessions'

    _unique_session_id = models.Constraint(
        'unique (unique_session_id)',
        "The Session ID must be unique!",
    )

    customer = fields.Char(string='Customer', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner')
    hotspot_user = fields.Char(string='Username', readonly=True)
    hotspot_user_id = fields.Many2one('radius_manager.hotspot_user', string='Hotspot User')
    calling_station_id = fields.Char(string='MAC Address', readonly=True)
    acct_session_id = fields.Char(string='Session ID', readonly=True)
    user_ip = fields.Char(string='User IP', readonly=True)
    host_ip = fields.Char(string='Host IP', readonly=True)
    status = fields.Char(string='Status', readonly=True)
    start_time = fields.Datetime(string='Start Time', readonly=True)
    end_time = fields.Datetime(string='End Time', readonly=True)
    terminate_cause = fields.Char(string='Terminate Cause', readonly=True)
    uptime = fields.Char(string='Uptime', readonly=True)
    download_amount = fields.Char(string='Download', readonly=True)
    download = fields.Integer(string='Download Amount', readonly=True)
    upload_amount = fields.Char(string='Upload', readonly=True)
    upload = fields.Integer(string='Upload Amount', readonly=True)
    transfer = fields.Integer(string='Transfer', readonly=True)
    transfer_amount = fields.Char(string='Transfer Amount', readonly=True)
    unique_session_id = fields.Char(string='Unique Session ID', readonly=True)

    _sql_constraints = [('unique_session_id_uniq', 'unique(unique_session_id)', 'Session ID must be unique')]

    @staticmethod
    def get_unique_session_id(nas_ip, acct_session_id, calling_station_id):
        """
        Get a unique session ID.
        """
        session_data = f"{nas_ip}-{acct_session_id}-{calling_station_id}"
        unique_session_id = hashlib.sha256(session_data.encode()).hexdigest()
        return unique_session_id

    def get_sessions(self):
        """
        Get all user sessions from the User Manager.
        """
        router.connect()
        sessions = router.get_active_sessions()

        try:
            sessions_list = []
            for session in sessions:
                del session['.id']

                unique_session_id = HotspotUserSession.get_unique_session_id(session['host-ip'],
                                                                             session['acct-session-id'],
                                                                             session['calling-station-id'])

                # Check if the session already exists
                if self.env['radius_manager.hotspot_user_session'].search_count(
                        [('unique_session_id', '=', unique_session_id)]) > 0:
                    logging.info(f"Session with unique_session_id {unique_session_id} already exists. Skipping.")
                    continue

                download = int(session['download'])
                upload = int(session['upload'])
                transfer = download + upload
                val = {
                    'unique_session_id': unique_session_id,
                    'customer': session['customer'],
                    'hotspot_user': session['user'],
                    'calling_station_id': session['calling-station-id'],
                    'acct_session_id': session['acct-session-id'],
                    'user_ip': session['user-ip'],
                    'host_ip': session['host-ip'],
                    'status': session['status'],
                    'start_time': convert_to_odoo_timestamp(session['from-time']),
                    'end_time': convert_to_odoo_timestamp(session['till-time']),
                    'uptime': session['uptime'],
                    'download': session['download'],
                    'download_amount': bytes_to_human_readable(download),
                    'upload': session['upload'],
                    'upload_amount': bytes_to_human_readable(upload),
                    'transfer': transfer,
                    'transfer_amount': bytes_to_human_readable(transfer)
                }
                if session.get('terminate-cause', None):
                    val['terminate_cause'] = session["terminate-cause"]

                partner = self.env['res.partner'].search([('kredoh_username', '=', session['customer'])], limit=1)
                if not partner:
                    logging.warning(f"HotspotUserSession::get_sessions Partner not found for {session['customer']}")
                else:
                    val['partner_id'] = partner.id

                hotspot_user = self.env['radius_manager.hotspot_user'].search([('username', '=', session['user'])],
                                                                              limit=1)
                if not hotspot_user:
                    logging.warning(f"HotspotUserSession::get_sessions Hotspot User not found for {session['user']}")
                else:
                    val['hotspot_user_id'] = hotspot_user.id

                logging.info(f"HotspotUserSession::get_sessions Session: {val}")

                if len(self.env['radius_manager.hotspot_user_session'].search(
                        [('unique_session_id', '=', unique_session_id)], limit=1)) == 0:
                    sessions_list.append(val)

            self.create(sessions_list)
        finally:
            router.disconnect()
            logging.info("Disconnected from MikroTik.")
