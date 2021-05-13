# -*- coding: utf-8 -*-
# from odoo import http


# class ReportPurchaseEmbarque(http.Controller):
#     @http.route('/report_purchase_embarque/report_purchase_embarque/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_purchase_embarque/report_purchase_embarque/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_purchase_embarque.listing', {
#             'root': '/report_purchase_embarque/report_purchase_embarque',
#             'objects': http.request.env['report_purchase_embarque.report_purchase_embarque'].search([]),
#         })

#     @http.route('/report_purchase_embarque/report_purchase_embarque/objects/<model("report_purchase_embarque.report_purchase_embarque"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_purchase_embarque.object', {
#             'object': obj
#         })
