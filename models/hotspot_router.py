import logging

from odoo import models, fields
from odoo.exceptions import ValidationError
from ..utils.router_manager import RouterManager
from .utils import bytes_to_human_readable


class HotspotRouter(models.Model):
    _name = 'radius_manager.hotspot_router'
    _description = 'Hotspot Router'

    name = fields.Char(string='Name', required=True)
    host = fields.Char(string='Host', required=True)
    port = fields.Integer(string='Port', required=True)
    username = fields.Char(string='Username', required=True)
    password = fields.Char(string='Password', required=True)
    model = fields.Char(string='Model', readonly=True)
    uptime = fields.Char(string='Uptime', readonly=True)
    cpu_load = fields.Char(string='CPU Load', readonly=True)
    free_memory = fields.Char(string='Free Memory', readonly=True)
    memory = fields.Char(string='Memory', readonly=True)
    memory_percentage = fields.Char(string='Memory Percentage', readonly=True)
    free_disk_space = fields.Char(string='Free Disk Space', readonly=True)
    disk_space = fields.Char(string='Disk Space', readonly=True)
    firmware_version = fields.Char(string='Firmware Version', readonly=True)
    architecture_name = fields.Char(string='Architecture Name', readonly=True)
    cpu_count = fields.Char(string='CPU Count', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', domain=[('is_kredoh_partner', '=', True)])

    def update_router_info(self):
        """
        Update the router information.
        """

        host = self.host
        port = self.port
        username = self.username
        password = self.password
        router = RouterManager(host=host, port=port, username=username, password=password, debug=True)

        router.connect()
        response = router.get_router_info()
        if len(response) == 2:
            error_msg = response[0]['']
            raise ValidationError(f"Failed to get router info: {error_msg}")
        logging.info(f"update_router_info::  response --> {response}")
        data = response[0]
        self.firmware_version = data.get("version")
        disk_space = bytes_to_human_readable(data.get("total-hdd-space"))
        self.disk_space = disk_space
        free_disk_space = bytes_to_human_readable(data.get("free-hdd-space"))
        self.free_disk_space = free_disk_space
        memory = bytes_to_human_readable(data.get("total-memory"))
        self.memory = memory
        free_memory = bytes_to_human_readable(data.get("free-memory"))
        self.free_memory = free_memory
        self.cpu_load = data.get("cpu-load")
        self.uptime = data.get("uptime")
        self.model = data.get("board-name")
        self.architecture_name = data.get("architecture-name")
        self.cpu_count = data.get("cpu-count")
