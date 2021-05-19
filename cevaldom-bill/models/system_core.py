# -*- coding: utf-8 -*-

from odoo import api, models, fields


class SystemCore(models.Model):
    _name = 'sistema.core'
    _description = 'Core integration with cevaldom information'

    account_move = fields.One2many('account.move', 'bill_id', string="Account move values")
    product = fields.One2many('product.product', 'bill_id', string="Product product Data")
    res_partner = fields.One2many('res.partner', 'bill_id', string="Partner Data")

