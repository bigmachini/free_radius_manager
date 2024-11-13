import logging

from odoo import models, fields
from odoo.exceptions import ValidationError
from .config import host, port, username, password
from ..utils.user_manager_packages import UserManagerPackages

router = UserManagerPackages(host=host, port=port, username=username, password=password, debug=True)


def float_time_to_str(float_time):
    if not float_time:
        return "0s"

    hours = int(float_time)
    minutes = int((float_time * 60) % 60)
    seconds = int((float_time * 3600) % 60)
    return f"{hours}h{minutes}m{seconds}s"


class HotspotPackage(models.Model):
    _name = 'radius_manager.hotspot_package'
    _description = 'Hotspot Package'

    name = fields.Char(string='Package Name', required=True)
    hotspot_profile_id = fields.Many2one('radius_manager.hotspot_profile', string='Hotspot Profile', required=True)
    hotspot_profile_limitation_id = fields.Many2one('radius_manager.hotspot_profile_limitation',
                                                    string='Hotspot Profile Limitation', required=True)

    from_time = fields.Float(string="From Time", required=True)
    till_time = fields.Float(string="Till Time", required=True)

    monday = fields.Boolean(string='Monday')
    tuesday = fields.Boolean(string='Tuesday')
    wednesday = fields.Boolean(string='Wednesday')
    thursday = fields.Boolean(string='Thursday')
    friday = fields.Boolean(string='Friday')
    saturday = fields.Boolean(string='Saturday')
    sunday = fields.Boolean(string='Sunday')
    hotspot_package_id = fields.Char(string='Hotspot Package ID', readonly=True)

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

        record = super(HotspotPackage, self).write(vals)
        return record

    def create_hotspot_package(self):
        """
        Create a new User Manager profile.
        """

        try:
            router.connect()

            package = router.get_package_by_name(self.hotspot_profile_id.name, self.hotspot_profile_limitation_id.name)
            if not package:
                response = router.create_package(
                    profile_name=self.hotspot_profile_id.name, limitation_name=self.hotspot_profile_limitation_id.name,
                    from_time=float_time_to_str(self.from_time), till_time=float_time_to_str(self.till_time),
                    weekdays=self.get_active_weekdays()
                )

                logging.info(f"Profile '{response}' created successfully!")

            package = router.get_package_by_name(self.hotspot_profile_id.name, self.hotspot_profile_limitation_id.name)
            logging.info(f"HotspotPackage::create_hotspot_package package --> {package}")
            if package:
                self.hotspot_package_id = package.get(".id")
            else:
                raise ValidationError(f"HotspotPackage::create_hotspot_package Package not created")
        except Exception as e:
            logging.error(f"HotspotPackage::create_hotspot_package Exception e -->{e}")
        finally:
            router.disconnect()

    def update_hotspot_package(self):
        """
        Update an existing Hotspot Package.
        """
        try:
            router.connect()
            package = router.get_package_by_name(self.hotspot_profile_id.name, self.hotspot_profile_limitation_id.name)
            if not package:
                raise ValidationError("Package does not exist.")

            response = router.update_package(
                id=self.hotspot_package_id,
                from_time=float_time_to_str(self.from_time),
                till_time=float_time_to_str(self.till_time),
                weekdays=self.get_active_weekdays()
            )

            logging.info(f"HotspotPackage::update_package  Profile '{response}' updated successfully!")
        except Exception as e:
            logging.error(f"HotspotPackage::update_package Exception e -->{e}")
        finally:
            router.disconnect()

    def delete_hotspot_package(self):
        """
        Delete an existing Hotspot Package.
        """
        try:
            router.connect()
            package = router.get_package_by_name(self.hotspot_profile_id.name, self.hotspot_profile_limitation_id.name)
            logging.info(f"HotspotPackage::delete_package  package {package}!")

            if not package:
                raise ValidationError("Package does not exist.")

            response = router.delete_package(self.hotspot_package_id)
            logging.info(f"HotspotPackage::delete_package  response {response}!")
        except Exception as e:
            logging.error(f"HotspotPackage::delete_package Exception e -->{e}")
        finally:
            router.disconnect()
