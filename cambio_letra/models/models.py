# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class cambio_letra(models.Model):
#     _name = 'cambio_letra.cambio_letra'
#     _description = 'cambio_letra.cambio_letra'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
