# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    id_billing_service = fields.Integer(string="ID BILLING SERVICE")
