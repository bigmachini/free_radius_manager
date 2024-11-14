import logging

from odoo import models, fields
from odoo.exceptions import ValidationError
from .config import host, port, username, password
from ..utils.user_manager_profile_limitation import UserManagerProfileLimitation

router = UserManagerProfileLimitation(host=host, port=port, username=username, password=password, debug=True)


def float_time_to_str(float_time):
    if not float_time:
        return "0s"

    hours = int(float_time)
    minutes = int((float_time * 60) % 60)
    seconds = int((float_time * 3600) % 60)
    return f"{hours}h{minutes}m{seconds}s"


class HotspotProfileLimitation(models.Model):
    _name = 'radius_manager.hotspot_profile_limitation'
    _description = 'Hotspot Profile Limitation'

    name = fields.Char(string='Package Name', required=True)
    hotspot_profile_id = fields.Many2one('radius_manager.hotspot_profile', string='Hotspot Profile')
    hotspot_limitation_id = fields.Many2one('radius_manager.hotspot_limitation',
                                            string='Hotspot Profile Limitation')

    from_time = fields.Float(string="From Time")
    till_time = fields.Float(string="Till Time")

    monday = fields.Boolean(string='Monday')
    tuesday = fields.Boolean(string='Tuesday')
    wednesday = fields.Boolean(string='Wednesday')
    thursday = fields.Boolean(string='Thursday')
    friday = fields.Boolean(string='Friday')
    saturday = fields.Boolean(string='Saturday')
    sunday = fields.Boolean(string='Sunday')
    hotspot_profile_limitation_id = fields.Char(string='Profile Limitation ID', readonly=True)

    def get_active_weekdays(self):
        """
        Generate a comma-separated string of active weekdays based on boolean fields.
        """
        weekdays = []
        if self.sunday:
            weekdays.append('sunday')
        if self.monday:
            weekdays.append('monday')
        if self.tuesday:
            weekdays.append('tuesday')
        if self.wednesday:
            weekdays.append('wednesday')
        if self.thursday:
            weekdays.append('thursday')
        if self.friday:
            weekdays.append('friday')
        if self.saturday:
            weekdays.append('saturday')

        return ','.join(weekdays)

    def write(self, vals):
        """
        Override the create method to create a new User Manager profile.
        """
        from_time = vals.get("from_time", None) or self.from_time
        till_time = vals.get("till_time", None) or self.till_time

        if from_time > till_time:
            raise ValidationError("The 'From Time' must be less than the 'Till Time'.")

        record = super(HotspotProfileLimitation, self).write(vals)
        return record

    def create_hotspot_profile_limitation(self):
        """
        Create a new User Manager profile.
        """

        try:
            router.connect()

            profile_limitation = router.get_profile_limitation_by_name(self.hotspot_profile_id.name,
                                                                       self.hotspot_limitation_id.name)
            if not profile_limitation:
                response = router.create_profile_limitation(
                    profile_name=self.hotspot_profile_id.name, limitation_name=self.hotspot_limitation_id.name,
                    from_time=float_time_to_str(self.from_time), till_time=float_time_to_str(self.till_time),
                    weekdays=self.get_active_weekdays()
                )

                logging.info(f"Profile '{response}' created successfully!")

            profile_limitation = router.get_profile_limitation_by_name(self.hotspot_profile_id.name,
                                                                       self.hotspot_limitation_id.name)
            logging.info(
                f"HotspotProfileLimitation::create_hotspot_profile_limitation profile_limitation --> {profile_limitation}")
            if profile_limitation:
                self.hotspot_profile_limitation_id = profile_limitation.get(".id")
            else:
                raise ValidationError(
                    f"HotspotProfileLimitation::create_hotspot_profile_limitation profile_limitation not created")
        except Exception as e:
            logging.error(f"HotspotProfileLimitation::create_hotspot_profile_limitation Exception e -->{e}")
        finally:
            router.disconnect()

    def update_hotspot_profile_limitation(self):
        """
        Update an existing Hotspot profile_limitation.
        """
        try:
            router.connect()
            profile_limitation = router.get_profile_limitation_by_name(self.hotspot_profile_id.name,
                                                                       self.hotspot_limitation_id.name)
            if not profile_limitation:
                raise ValidationError("profile_limitation does not exist.")

            response = router.update_profile_limitation(
                profile_limitation_id=self.hotspot_profile_limitation_id,
                from_time=float_time_to_str(self.from_time),
                till_time=float_time_to_str(self.till_time),
                weekdays=self.get_active_weekdays()
            )

            logging.info(
                f"HotspotProfileLimitation::update_profile_limitation  Profile '{response}' updated successfully!")
        except Exception as e:
            logging.error(f"HotspotProfileLimitation::update_profile_limitation Exception e -->{e}")
        finally:
            router.disconnect()

    def delete_hotspot_profile_limitation(self):
        """
        Delete an existing Hotspot profile_limitation.
        """
        try:
            router.connect()
            profile_limitation = router.get_profile_limitation_by_name(self.hotspot_profile_id.name,
                                                                       self.hotspot_limitation_id.name)
            logging.info(
                f"HotspotProfileLimitation::delete_profile_limitation  profile_limitation {profile_limitation}!")

            if not profile_limitation:
                raise ValidationError("profile_limitation does not exist.")

            response = router.delete_profile_limitation(self.hotspot_profile_limitation_id)
            self.hotspot_profile_limitation_id = None
            logging.info(f"HotspotProfileLimitation::delete_profile_limitation  response {response}!")
        except Exception as e:
            logging.error(f"HotspotProfileLimitation::delete_profile_limitation Exception e -->{e}")
        finally:
            router.disconnect()
