# -*- coding: utf-8 -*-
# from odoo import http


# class UnitNoItbis(http.Controller):
#     @http.route('/unit_no_itbis/unit_no_itbis/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/unit_no_itbis/unit_no_itbis/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('unit_no_itbis.listing', {
#             'root': '/unit_no_itbis/unit_no_itbis',
#             'objects': http.request.env['unit_no_itbis.unit_no_itbis'].search([]),
#         })

#     @http.route('/unit_no_itbis/unit_no_itbis/objects/<model("unit_no_itbis.unit_no_itbis"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('unit_no_itbis.object', {
#             'object': obj
#         })
