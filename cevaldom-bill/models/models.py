# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BillResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'cevaldom-bill'

    bill_id = fields.Many2one('sistema.core')
    entity_code = fields.Char(string="ENTITY CODE")
    person_type = fields.Selection([
        ('natural', 'NATURAL'),
        ('juridica', 'JURIDICA')
    ], string="PERSON TYPE")
    document_type = fields.Char(string="DOCUMENT TYPE")

    entity_name = fields.Char(string="ENTITY NAME")
    entity_address = fields.Char(string="ENTITY ADDRESS")
    entity_district = fields.Char(string="ENTITY DISTRICT")
    entity_province = fields.Char(string="ENTITY PROVINCE")
    entity_country = fields.Char(string="ENTITY COUNTRY")
    entity_type = fields.Integer(string="ENTITY TYPE")
    entity_collection = fields.Selection([
        ('titulares', 'TITULARES'),
        ('participantes', 'PARTICIPANTES'),
        ('emisores', 'EMISORES')
    ], string="ENTITY COLLECTION")
    id_holder = fields.Integer(string="ID HOLDER")
    id_issuer = fields.Char(string="ID ISSUER")
    id_participant = fields.Integer(string="ID PARTICIPANT")
    id_entity_block = fields.Integer(string="ID ENTITY BLOCK")


class BillAccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Bill calculation account move'

    bill_id = fields.Many2one('sistema.core')
    id_billing_service = fields.Integer(string="ID BILLING SERVICE")


class BillProduct(models.Model):
    _inherit = 'product.template'
    _description = 'Bill calculation product product'

    bill_id = fields.Many2one('sistema.core')
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


class BillConfig(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = 'Bill Calculus config'

    bill_host = fields.Char(string="Host")
    bill_port = fields.Char(string="Port")
    bill_user = fields.Char(string="User")
    bill_pass = fields.Char(string="Password")
    bill_db_name = fields.Char(string="Database Name")

    def get_values(self):
        res = super(BillConfig, self).get_values()
        res.update(
            bill_host=self.env['ir.config_parameter'].sudo().get_param('cevaldom-bill.bill_host'),
            bill_port=self.env['ir.config_parameter'].sudo().get_param('cevaldom-bill.bill_port'),
            bill_user=self.env['ir.config_parameter'].sudo().get_param('cevaldom-bill.bill_user'),
            bill_pass=self.env['ir.config_parameter'].sudo().get_param('cevaldom-bill.bill_pass'),
            bill_db_name=self.env['ir.config_parameter'].sudo().get_param('cevaldom-bill.bill_db_name')
        )
        return res

    def set_values(self):
        super(BillConfig, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('cevaldom-bill.bill_host', self.bill_host)
        self.env['ir.config_parameter'].sudo().set_param('cevaldom-bill.bill_port', self.bill_port)
        self.env['ir.config_parameter'].sudo().set_param('cevaldom-bill.bill_user', self.bill_user)
        self.env['ir.config_parameter'].sudo().set_param('cevaldom-bill.bill_pass', self.bill_pass)
        self.env['ir.config_parameter'].sudo().set_param('cevaldom-bill.bill_db_name', self.bill_db_name)
