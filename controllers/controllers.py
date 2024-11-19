# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request
from .utils import validate_mac_address

HEADERS = [('Content-Type', 'application/json'),
           ('Cache-Control', 'no-store')]


class RadiusManagerAPI(http.Controller):
    @http.route('/api/user/<mac>', auth='public', type='http', csrf=False)
    def check_for_user(self, mac, **kw):
        logging.info(f'RadiusManagerAPI::check_for_user::  mac --> {mac}')

        hotspot_user = request.env['radius_manager.hotspot_user'].sudo().search(
            [('username', '=', mac)], limit=1)
        if not hotspot_user:
            data = {'status': False, 'message': 'User not found', 'data': {}}
            return request.make_response(json.dumps(data), HEADERS, status=404)

        hotspot_user.clear_user_profile()

        data = {'status': True, 'message': '', 'data': {}}
        return request.make_response(json.dumps(data), HEADERS, status=200)

    @http.route('/api/user/profile/clear', auth='public', type='http', methods=['POST'], csrf=False)
    def clear_user_profile(self, **kw):
        logging.info(f'RadiusManagerAPI::clear_user_profile::')

        data = json.loads(request.httprequest.data)
        logging.info(f'RadiusManagerAPI::clear_user_profile:: data --> {data}')

        hotspot_user = request.env['radius_manager.hotspot_user'].sudo().search(
            [('username', '=', data['mac'])], limit=1)
        if not hotspot_user:
            data = {'status': False, 'message': 'User not found', 'data': {}}
            return request.make_response(json.dumps(data), HEADERS, status=404)

        hotspot_user.clear_user_profile()

        data = {
            'status': True,
            'message': 'Clear Profile Successfully',
            'data': {
                'user_id': hotspot_user.id,
            }
        }
        return request.make_response(json.dumps(data), HEADERS, status=200)

    @http.route('/api/user/profile/<mac>', auth='public', type='http')
    def get_user_profile(self, mac, **kw):
        logging.info(f'RadiusManagerAPI::get_user_profile:: mac --> {mac}')

        hotspot_user = request.env['radius_manager.hotspot_user'].sudo().search(
            [('username', '=', mac)], limit=1)
        if not hotspot_user:
            data = {'status': False, 'message': 'User not found', 'data': {}}
            return request.make_response(json.dumps(data), HEADERS, status=404)

        user_profile_limitation = request.env['radius_manager.user_profile_limitation'].sudo().search(
            [('hotspot_user_id', '=', hotspot_user.id), ('is_activated', '=', True)], limit=1)
        if not user_profile_limitation:
            data = {'status': False, 'message': 'Profile limitation not found', 'data': {}}
            return request.make_response(json.dumps(data), HEADERS, status=404)

        data = {
            'status': True,
            'message': 'Active Profile Found',
            'data': {
                'user_id': hotspot_user.id,
            }
        }
        return request.make_response(json.dumps(data), HEADERS, status=200)

    @http.route('/api/user/packages/<partner_id>', auth='public', type='http')
    def get_user_packages(self, partner_id, **kw):
        logging.info(f'RadiusManagerAPI::get_packages:: partner_id --> {partner_id}')

        partner = request.env['res.partner'].sudo().browse(int(partner_id))
        if not partner:
            data = {'status': False, 'message': 'Partner not found', 'data': {}}
            return request.make_response(data, HEADERS, status=404)

        hotspot_profile_limitations = request.env['radius_manager.hotspot_profile_limitation'].sudo().search(
            [('partner_id', '=', partner.id)], order='id desc')

        response = []
        for profile_limitation in hotspot_profile_limitations:
            response.append({
                'id': profile_limitation.id,
                'name': profile_limitation.name,
                'uptime': profile_limitation.hotspot_limitation_id.uptime_limit,
            })

        data = json.dumps({'status': True, 'message': 'Packages retrieved successfully', 'data': response})
        return request.make_response(data, HEADERS, status=200)

    @http.route('/api/user/subscribe', auth='public', type='http', methods=['POST'], csrf=False)
    def user_subscribe(self, **kw):
        logging.info(f'RadiusManagerAPI::user_subscribe:: ')

        data = json.loads(request.httprequest.data)
        logging.info(f'RadiusManagerAPI::user_subscribe:: data --> {data}')

        # validate missing fields
        missing_fields = [field for field in ['mac_address', 'phone_number', 'package_id', 'partner_id'] if
                          field not in data]
        if missing_fields:
            response = {
                'status': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'data': {}
            }
            return request.make_response(json.dumps(response), HEADERS, status=400)
        if not validate_mac_address(data['mac_address']):
            response = {
                'status': False,
                'message': 'Invalid MAC address format',
                'data': {}
            }
            return request.make_response(json.dumps(response), HEADERS, status=400)

        mac_address = data['mac_address']
        hotspot_user = request.env['radius_manager.hotspot_user'].sudo().search(
            [('username', '=', mac_address)], limit=1)

        logging.info(f'RadiusManagerAPI::user_subscribe:: hotspot_user --> {hotspot_user}')

        if not hotspot_user:
            partner = request.env['res.partner'].sudo().browse(int(data['partner_id']))
            if not partner:
                data = {'status': False, 'message': 'Partner not found', 'data': {}}
                return request.make_response(json.dumps(data), HEADERS, status=404)

            hotspot_user = request.env['radius_manager.hotspot_user'].sudo().create({
                "username": mac_address,
                "phone": data['phone_number'],
                "partner_id": partner.id,
                "name": mac_address
            })

            hotspot_user.create_hotspot_user()

        profile_limitation = request.env['radius_manager.hotspot_profile_limitation'].sudo().search(
            [('id', '=', data["package_id"])], limit=1)
        logging.info(f'RadiusManagerAPI::user_subscribe:: profile_limitation --> {profile_limitation}')

        if not profile_limitation:
            data = {'status': False, 'message': 'Package not found', 'data': {}}
            return request.make_response(json.dumps(data), HEADERS, status=404)


        vals = {
            'hotspot_profile_limitation_id': profile_limitation.id,
            'hotspot_user_id': hotspot_user.id,
        }
        user_profile_limitation = request.env['radius_manager.user_profile_limitation'].sudo().create([vals])
        if not user_profile_limitation:
            response = {
                'status': False,
                'message': 'Failed to subscribe user to package',
                'data': {}
            }
            return request.make_response(json.dumps(response), HEADERS, status=400)

        vals = {
            'user_profile_limitation_id': user_profile_limitation.id,
            'hotspot_user_id': hotspot_user.id,
            'amount': profile_limitation.hotspot_profile_id.price
        }
        incoming_payment = request.env['radius_manager.incoming_payments'].sudo().create([vals])



        # wizard = request.env['radius_manager.assign_user_profile_wizard'].sudo().create({
        #     'hotspot_profile_limitation_id': profile_limitation.id,
        #     'hotspot_user_id': hotspot_user.id
        # })
        # wizard.assign_profile()

        response = {
            'status': True,
            'message': 'User signed in successfully',
            'data': {
                'user_id': hotspot_user.id,
                'username': hotspot_user.username
            }
        }
        return request.make_response(json.dumps(response), HEADERS, status=200)
