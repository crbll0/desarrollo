# -*- coding: utf-8 -*-

import csv
import logging
from collections import namedtuple

from odoo import api, models, fields
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


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
    
    def clean_dict(self, dictionary, fields_list):
        d = dictionary.copy()
        for k in dictionary.keys():
            if k not in fields_list:
                del d[k]
        return d
    
    def import_data(self):
        csv_data = get_module_resource('cevaldom-bill', 'models/', 'core_system_data.csv')
        
        fields_core_lines = self.env['core.system.lines'].fields_get().keys()
        
        lines = []
        with open(csv_data, 'r') as f:
            reader = csv.DictReader(f)

            for i in reader:
                
                d = self.clean_dict(dict(i), fields_core_lines)
                lines.append((0, 0, d))
#         _logger.info(lines)    
        self.line_ids = lines


class CoreSystemLines(models.Model):
    _name = 'core.system.lines'
    _description = 'Core System Lines'
    
    core_id = fields.Many2one("core.system")
    
    # AccounMove Fields-------------------------------
    id_billing_calc_process = fields.Char()
    process_date = fields.Date(string="PROCESS DATE")
    processed_state = fields.Selection([
        ('PRELIMINAR', 'PRELIMINAR'),
        ('DEFINITIVO', 'DEFINITIVO')
    ], string="PROCESSED STATE")
    billing_period = fields.Selection([
        ('DIARIO', 'DIARIO'),
        ('MENSUAL', 'MENSUAL'),
        ('EVENTUAL', 'EVENTUAL')
        ], string="BILLING PERIOD")
    id_billing_calculation = fields.Integer(string="ID BILLING CALCULATION")
    payment_reference = fields.Char(string="PAYMENT REFERENCE")
    billing_date = fields.Date(string="BILLING DATE")
    billing_currency = fields.Selection([
        ('DOP', 'DOP'),
        ('USD', 'USD'),
        ('EUR', 'EUR')
    ],string="BILLING CURRENCY")
    ind_invoice_core = fields.Integer(string="IND INVOICE CORE")
    ind_web_service = fields.Integer(string="IND WEB SERVICE")
    ind_reject_core = fields.Integer(string="IND REJECT CORE")
    id_billing_detail = fields.Integer(string="ID BILLING DETAIL")
    service_rate = fields.Float(string="SERVICE RATE")
    quantity = fields.Float(string="QUANTITY")
    net_amount = fields.Float(string="NET AMOUNT")
    
    # ProducProduct Fields-------------------------------
    id_billing_service = fields.Integer(string="ID BILLING SERVICE")

    # ResPartner Fields-------------------------------
    entity_code = fields.Char(string="ENTITY CODE")
    person_type = fields.Selection([
        ('NATURAL', 'NATURAL'),
        ('JURIDICO', 'JURIDICA')
    ], string="PERSON TYPE")
    document_type = fields.Char(string="DOCUMENT TYPE")

    entity_name = fields.Char(string="ENTITY NAME")
    entity_address = fields.Char(string="ENTITY ADDRESS")
    entity_district = fields.Char(string="ENTITY DISTRICT")
    entity_province = fields.Char(string="ENTITY PROVINCE")
    entity_country = fields.Char(string="ENTITY COUNTRY")
    entity_type = fields.Integer(string="ENTITY TYPE")
    entity_collection = fields.Selection([
        ('TITULARES', 'TITULARES'),
        ('PARTICIPANTES', 'PARTICIPANTES'),
        ('EMISORES', 'EMISORES')
    ], string="ENTITY COLLECTION")
    id_holder = fields.Integer(string="ID HOLDER")
    id_issuer = fields.Char(string="ID ISSUER")
    id_participant = fields.Integer(string="ID PARTICIPANT")
    id_entity_block = fields.Integer(string="ID ENTITY BLOCK")