from datetime import timedelta, datetime

from odoo import models, fields, api

PROFILE_STATUS = [
    ('pending', 'Pending'),
    ('canceled', 'Cancelled'),
    ('active', 'Activated'),
    ('expired', 'Expired'),
]

#pending - payment has been initiated but not yet completed
#canceled - payment not processed
#active - payment processed and profile activated
#expired - profile expired


class UserProfileLimitation(models.Model):
    _name = 'radius_manager.user_profile_limitation'
    _description = 'User Profile Limitation'

    name = fields.Char(string="Name", compute='_compute_name', readonly=True)
    hotspot_profile_limitation_id = fields.Many2one('radius_manager.hotspot_profile_limitation',
                                                    string="Hotspot Profile Limitation", readonly=True)
    hotspot_user_id = fields.Many2one('radius_manager.hotspot_user', string="Hotspot User", readonly=True)
    download_speed = fields.Char(related='hotspot_profile_limitation_id.hotspot_limitation_id.rate_limit_rx', )
    upload_speed = fields.Char(related='hotspot_profile_limitation_id.hotspot_limitation_id.rate_limit_tx', )
    validity = fields.Char(related='hotspot_profile_limitation_id.hotspot_profile_id.validity')
    start_time = fields.Datetime(string="Start Time", readonly=True)
    end_time = fields.Datetime(string="Expiry Time", readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True,
                                 domain=[('is_kredoh_partner', '=', True)],
                                 readonly=True,
                                 default=lambda self: self.env.user.partner_id.id)

    profile_status = fields.Selection(PROFILE_STATUS, string="Profile Status", default='pending')
    time_left = fields.Char(string="Time Left", compute='_compute_time_left', store=True)

    @api.depends('end_time')
    def _compute_time_left(self):
        for record in self:
            if record.end_time:
                now = datetime.now()
                delta = record.end_time - now
                hours, remainder = divmod(delta.total_seconds(), 3600)
                minutes, seconds = divmod(remainder, 60)
                record.time_left = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
            else:
                record.time_left = "0h 0m 0s"

    @api.depends('hotspot_user_id.name', 'hotspot_profile_limitation_id.name')
    def _compute_name(self):
        for record in self:
            record.name = f'{record.hotspot_user_id.name} - {record.hotspot_profile_limitation_id.name}'

    def activate_profile(self):
        self.ensure_one()
        self.start_time = fields.Datetime.now()
        if self.validity[-1].lower() == 'd':
            self.end_time = self.start_time + timedelta(days=int(self.validity[:-1]))
        elif self.validity[-1].lower() == 'm':
            self.end_time = self.start_time + timedelta(minutes=int(self.validity[:-1]))
        elif self.validity[-1].lower() == 'h':
            self.end_time = self.start_time + timedelta(hours=int(self.validity[:-1]))

        self.hotspot_user_id.assign_profile_user(self.hotspot_profile_limitation_id.hotspot_profile_id.name)
