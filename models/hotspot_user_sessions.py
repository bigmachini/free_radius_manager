import hashlib
import logging

from odoo import models, fields
from .config import host, port, username, password
from .utils import convert_to_odoo_timestamp, bytes_to_human_readable
from ..utils.user_manager_sessions import HotspotSessionManager

router = HotspotSessionManager(host=host, port=port, username=username, password=password, debug=True)


class HotspotUserSession(models.Model):
    _name = 'radius_manager.hotspot_user_session'
    _description = 'User Sessions'

    _unique_session_id = models.Constraint(
        'unique (unique_session_id)',
        "The Session ID must be unique!",
    )

    customer = fields.Char(string='Customer', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
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
    nas_port = fields.Char(string='NAS Port', readonly=True)

    @staticmethod
    def get_unique_session_id(nas_port, acct_session_id, calling_station_id):
        """
        Get a unique session ID.
        """
        if not acct_session_id:
            session_data = f"{nas_port}-{calling_station_id}"
        else:
            session_data = f"{nas_port}-{acct_session_id}-{calling_station_id}"

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

                unique_session_id = HotspotUserSession.get_unique_session_id(session.get('nas-port', None),
                                                                             session.get('acct-session-id', None),
                                                                             session.get('calling-station-id', None))

                # Check if the session already exists

                download = int(session['download'])
                upload = int(session['upload'])
                transfer = download + upload
                val = {
                    'unique_session_id': unique_session_id,
                    'customer': session.get('customer', None),
                    'hotspot_user': session.get('user', None),
                    'calling_station_id': session.get('calling-station-id', None),
                    'acct_session_id': session.get('acct-session-id', None),
                    'user_ip': session.get('user-ip', None),
                    'host_ip': session.get('host-ip', None),
                    'status': session.get('status', None),
                    'start_time': convert_to_odoo_timestamp(session.get('from-time', None)),
                    'end_time': convert_to_odoo_timestamp(session.get('till-time', None)),
                    'uptime': session.get('uptime', None),
                    'download': session.get('download', None),
                    'download_amount': bytes_to_human_readable(download),
                    'upload': session.get('upload', None),
                    'upload_amount': bytes_to_human_readable(upload),
                    'transfer': transfer,
                    'transfer_amount': bytes_to_human_readable(transfer),
                    'nas_port': session.get('nas-port', None),
                }
                if session.get('terminate-cause', None):
                    val['terminate_cause'] = session.get("terminate-cause", None),

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

                session = self.env['radius_manager.hotspot_user_session'].search(
                    [('unique_session_id', '=', unique_session_id)], limit=1)

                if session:
                    logging.info(f"HotspotUserSession::get_sessions Updating session for {session['customer']}")
                    session.write(val)
                else:
                    logging.info(f"HotspotUserSession::get_sessions Creating session for {session['customer']}")
                    sessions_list.append(val)

            self.create(sessions_list)
        finally:
            router.disconnect()
            logging.info("Disconnected from MikroTik.")
