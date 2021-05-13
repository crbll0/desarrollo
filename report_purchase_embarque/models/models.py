# -*- coding: utf-8 -*-

from odoo import models, fields, api


class report_purchase_embarque(models.Model):
    _name = 'purchase.embarque'
    _description = 'Reporte Embarque Mercancia'

#     @api.depends('line_ids')
#     def _compute_line_count(self):
#         pass
#         for r in self:
#             r.line_count = 0#len(r.line_ids)
            
    name = fields.Char()
    date = fields.Date(default=fields.Date.today())
    lines_count = fields.Integer()#ompute='_compute_line_count')

    line_ids = fields.One2many('purchase.embarque.lines', 'report_id')
    
    def get_lines(self):
        purchase_lines = self.env['purchase.order.line'].search([
            ('order_id.state', 'in', ['purchase', 'done'])
        ]).filtered(lambda l: l.product_qty != l.qty_received)
        
        lines = []
        for line in purchase_lines:
            purchase_id = line.order_id
            lines.append((0, 0, {
                'partner_id': purchase_id.partner_id.id,
                'product_id': line.product_id.id,
                'purchase_id': purchase_id.id,
                'date': purchase_id.date_order,
                'qty_hand': 0, #line.product_id,
                'purchase_qty': line.product_qty,
                'qty_available_seller': 0,#ine.qty_available_seller,
                'qty_pending': 0,#line.qty_pending,
            }))
        
        self.line_ids = lines
        
    def action_view_lines(self):
        action = {
            'name': 'Detalle',
            'view_mode': 'tree',
            'res_model': 'purchase.embarque.lines',
            'type': 'ir.actions.act_window',
            'view_id': self.env.ref('report_purchase_embarque.embarque_lines_tree').id,
            'domain': [('report_id', '=', self.id)]
        }
        
        return action
    
    
class EmbarqueLines(models.Model):
    _name = 'purchase.embarque.lines'
    _description = 'Reporte Embarque Mercancia Lineas'
    
    report_id = fields.Many2one('purchase.embarque')
    
    partner_id = fields.Many2one('res.partner')
    product_id = fields.Many2one('product.product')
    purchase_id = fields.Many2one('purchase.order')
    date = fields.Datetime()
    qty_hand = fields.Float()
    purchase_qty = fields.Float()
    qty_available_seller = fields.Float()
    qty_pending = fields.Float()
    to_embarque = fields.Float()
