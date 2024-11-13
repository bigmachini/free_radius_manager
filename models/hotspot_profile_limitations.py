from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ..utils.usermanager_limitations import UserManagerLimitations
from .config import host, port, username, password
import logging

router = UserManagerLimitations(host=host, port=port, username=username, password=password, debug=True)


class HotspotProfileLimitation(models.Model):
    _name = 'radius_manager.hotspot_profile_limitation'
    _description = 'Profile Limitation'

    name = fields.Char(string='Limitation Name', required=True, help='The name of the profile limitation')
    rate_limit_rx = fields.Char(string='Rate Limit Download', required=True, help="""
    Sets the bandwidth limitation for the profile.
    
		Allowed Values:
	     Format: <Rx>
		    Rx: Download speed.
		    
		Units:
	    	k for kilobits per second (e.g., 512k).
	        M for megabits per second (e.g., 10M).
		    G for gigabits per second (e.g., 1G).
		    
		Example: 10M/5M (10 Mbps download, 5 Mbps upload).""")
    rate_limit_tx = fields.Char(string='Rate Limit Upload', required=True, help="""
        Sets the bandwidth limitation for the profile.

    		Allowed Values:
    	     Format: <Tx>
    		    Tx: Upload speed.

    		Units:
    	    	k for kilobits per second (e.g., 512k).
    	        M for megabits per second (e.g., 10M).
    		    G for gigabits per second (e.g., 1G).

    		Example: 10M/5M (10 Mbps download, 5 Mbps upload).""")
    uptime_limit = fields.Char(string='Uptime Limit', required=True, help="""
    The total time a user can stay online.
    
	   Allowed Values:
            Format: <D H:M:S>
                D: Days.
                H: Hours.
                M: Minutes.
                S: Seconds.
                
		Special Value: unlimited (no uptime restriction).
		
		Example: 1h30m (1 hour, 30 minutes).""")
    transfer_limit = fields.Char(string='Transfer Limit', required=True, help="""
    The total data the user can upload and download.
    
		Allowed Values:
		    Format: <size>
		    Units: B (bytes), k (kilobytes), M (megabytes), G (gigabytes), T (terabytes).
	        Special Value: unlimited (no data restriction).
	        
		Example: 1G (1 GB).""")
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, domain=[('is_kredoh_partner', '=', True)])
    hotspot_profile_limitation_id = fields.Char(string="Hotspot Profile Limitation ID", readonly=True)

    def create_profile_limitation(self):
        """
        Create a new User Manager profile limitation.
        """
        if not self.partner_id.kredoh_username:
            raise ValidationError("The partner does not have a Kredoh username.")

        try:
            router.connect()

            response = router.add_limitation(name=self.name, rate_limit_tx=self.rate_limit_tx,
                                             rate_limit_rx=self.rate_limit_rx, uptime_limit=self.uptime_limit,
                                             transfer_limit=self.transfer_limit, owner=self.partner_id.kredoh_username)
            logging.info(f"Profile limitation '{response}' created successfully!")
            profile_limitation = router.get_limitation_by_name(self.name)
            logging.info(f"Profile limitation: {profile_limitation}")
            if profile_limitation:
                self.hotspot_profile_limitation_id = profile_limitation.get(".id")
        except Exception as e:
            logging.error(f"Error creating hotspot profile limitation: {e}")

    @api.model_create_multi
    def create(self, vals_list):
        res = super(HotspotProfileLimitation, self).create(vals_list)
        return res

    def write(self, vals):
        res = super(HotspotProfileLimitation, self).write(vals)
        return res
