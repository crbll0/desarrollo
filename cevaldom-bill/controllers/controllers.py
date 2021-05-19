# -*- coding: utf-8 -*-
# from odoo import http


# class Cevaldom-bill(http.Controller):
#     @http.route('/cevaldom-bill/cevaldom-bill/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cevaldom-bill/cevaldom-bill/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cevaldom-bill.listing', {
#             'root': '/cevaldom-bill/cevaldom-bill',
#             'objects': http.request.env['cevaldom-bill.cevaldom-bill'].search([]),
#         })

#     @http.route('/cevaldom-bill/cevaldom-bill/objects/<model("cevaldom-bill.cevaldom-bill"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cevaldom-bill.object', {
#             'object': obj
#         })
