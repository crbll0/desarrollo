# -*- coding: utf-8 -*-
# from odoo import http


# class CambioLetra(http.Controller):
#     @http.route('/cambio_letra/cambio_letra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cambio_letra/cambio_letra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cambio_letra.listing', {
#             'root': '/cambio_letra/cambio_letra',
#             'objects': http.request.env['cambio_letra.cambio_letra'].search([]),
#         })

#     @http.route('/cambio_letra/cambio_letra/objects/<model("cambio_letra.cambio_letra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cambio_letra.object', {
#             'object': obj
#         })
