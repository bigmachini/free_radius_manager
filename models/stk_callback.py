import logging

from odoo import models, fields, api
from datetime import datetime


class STKCallback(models.Model):
    _inherit = 'safaricom_stk.stk_callback'

    @api.model
    def create_from_json(self, data):
        stk_callback = super(STKCallback, self).create_from_json(data)
        logging.info(f'STKCallback::create_from_json  stk_callback: {stk_callback}')

        if stk_callback and stk_callback.result_code == 0:
            logging.info(f'STKCallback::create_from_json  stk_callback.result_code : {stk_callback.result_code}')
            user_profile_limitation_id = stk_callback.stk_request_id.user_profile_limitation_id
            logging.info(f'STKCallback::create_from_json  user_profile_limitation_id : {user_profile_limitation_id}')

            if user_profile_limitation_id:
                user_profile_limitation_id.activate_profile()
