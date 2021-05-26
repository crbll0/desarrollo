# -*- coding: utf-8 -*-

from odoo import api, models, fields


class CoreSystem(models.Model):
    _name = 'core.system'
    _description = 'Core System'
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate'),
        ('done', 'Done')
    ], default='draft')
    
    date = fields.Date(string="Date")
    line_ids = fields.One2many('core.system.lines', 'core_id')


class CoreSystemLines(models.Model):
    _name = 'core.system.lines'
    _description = 'Core System Lines'
    
    core_id = fields.Many2one("core.system")
    
    # AccounMove Fields-------------------------------
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
    
    # ProducProduct Fields-------------------------------
    id_billing_service = fields.Integer(string="ID BILLING SERVICE")

    # ResPartner Fields-------------------------------
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