# -*- coding: utf-8 -*-
# from odoo import http


# class CuadreCaja(http.Controller):
#     @http.route('/cuadre_caja/cuadre_caja/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cuadre_caja/cuadre_caja/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cuadre_caja.listing', {
#             'root': '/cuadre_caja/cuadre_caja',
#             'objects': http.request.env['cuadre_caja.cuadre_caja'].search([]),
#         })

#     @http.route('/cuadre_caja/cuadre_caja/objects/<model("cuadre_caja.cuadre_caja"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cuadre_caja.object', {
#             'object': obj
#         })
