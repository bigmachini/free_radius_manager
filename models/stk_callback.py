import logging

from odoo import models, api


class STKCallback(models.Model):
    _inherit = 'safaricom_stk.stk_callback'

    @api.model
    def create_from_json(self, data):
        stk_callback = super(STKCallback, self).create_from_json(data)
        logging.info(f'STKCallback::create_from_json  ++++ stk_callback: {stk_callback}')

        # Check if the stk_callback is not None
        if stk_callback:
            logging.info(f'STKCallback::create_from_json  ++++ stk_callback.result_code : {stk_callback.result_code}')
            user_profile_limitation_id = stk_callback.stk_request_id.user_profile_limitation_id
            logging.info(f'STKCallback::create_from_json  ++++ user_profile_limitation_id : {user_profile_limitation_id}')

            # Check if the result code is 0 - activate profile else cancel the profile
            if stk_callback.result_code == 0:
                user_profile_limitation_id.activate_profile()
            else:
                user_profile_limitation_id.profile_status = 'canceled'

        return stk_callback
