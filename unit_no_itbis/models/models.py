# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class unit_no_itbis(models.Model):
#     _name = 'unit_no_itbis.unit_no_itbis'
#     _description = 'unit_no_itbis.unit_no_itbis'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
