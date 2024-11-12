# -*- coding: utf-8 -*-
# from odoo import http


# class FreeRadiusManager(http.Controller):
#     @http.route('/free_radius_manager/free_radius_manager', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/free_radius_manager/free_radius_manager/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('free_radius_manager.listing', {
#             'root': '/free_radius_manager/free_radius_manager',
#             'objects': http.request.env['free_radius_manager.free_radius_manager'].search([]),
#         })

#     @http.route('/free_radius_manager/free_radius_manager/objects/<model("free_radius_manager.free_radius_manager"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('free_radius_manager.object', {
#             'object': obj
#         })

