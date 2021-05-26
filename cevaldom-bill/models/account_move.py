# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    process_date = fields.Date(string="PROCESS DATE")
    processed_state = fields.Selection([
        ('preliminar', 'PRELIMINAR'),
        ('definitivo', 'DEFINITIVO')
    ], string="PROCESSED STATE")
    billing_period = fields.Selection([
        ('diario', 'DIARIO'),
        ('mensual', 'MENSUAL'),
        ('eventual', 'EVENTUAL')
        ], string="BILLING PERIOD")
    id_billing_calculation = fields.Integer(string="ID BILLING CALCULATION")
    payment_reference = fields.Char(string="PAYMENT REFERENCE")
    billing_date = fields.Date(string="BILLING DATE")
    billing_currency = fields.Selection([
        ('dop', 'DOP'),
        ('usd', 'USD'),
        ('eur', 'EUR')
    ],string="BILLING CURRENCY")
    ind_invoice_core = fields.Integer(string="IND INVOICE CORE")
    ind_web_service = fields.Integer(string="IND WEB SERVICE")
    ind_reject_core = fields.Integer(string="IND REJECT CORE")
    id_billing_detail = fields.Integer(string="ID BILLING DETAIL")
    service_rate = fields.Integer(string="SERVICE RATE")
    quantity = fields.Integer(string="QUANTITY")
    net_amount = fields.Integer(string="NET AMOUNT")
