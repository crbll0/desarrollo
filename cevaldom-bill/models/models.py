# -*- coding: utf-8 -*-

import csv
import logging
from collections import namedtuple

from odoo import api, models, fields
from odoo.tools.misc import groupby
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)


class CoreSystem(models.Model):
    _name = 'core.system'
    _description = 'Core System'
    _inherit = ['mail.thread']
    
    
    @api.depends('move_ids')
    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(rec.move_ids)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('import', 'Import'),
        ('validate', 'Validate'),
        ('done', 'Done')
    ], default='draft')
    
    date = fields.Date(string="Date")
    move_count = fields.Integer('Invoice Count', compute='_compute_move_count')
    move_ids = fields.One2many('account.move', 'core_id')
    line_ids = fields.One2many('core.system.lines', 'core_id')
    
    
    def clean_dict(self, dictionary, fields_list):
        d = dictionary.copy()
        for k in dictionary.keys():
            if k not in fields_list:
                del d[k]
                
        return d
    
    def action_import(self):
        csv_data = get_module_resource('cevaldom-bill', 'models/', 'core_system_data.csv')
        
        fields_core_lines = self.env['core.system.lines'].fields_get().keys()
        
        lines = []
        with open(csv_data, 'r') as f:
            reader = csv.DictReader(f)

            for i in reader:
                d = self.clean_dict(dict(i), fields_core_lines)
                lines.append((0, 0, d))

        self.line_ids = lines
        self.state = 'import'

    def action_validate(self):
        Product = self.env['product.product']
        Partner = self.env['res.partner']
        
        service_worked = []
        partner_worked = []
        sc = []
        pc = []
        for line in self.line_ids:
            if line.id_billing_service not in service_worked:
                if not Product.search([('id_billing_service', '=', line.id_billing_service)]):
                    service_created = Product.create({
                        'id_billing_service': line.id_billing_service,
                        'type': 'service',
                        'default_code': line.id_billing_service,
                        'name': 'Servicio ' + str(line.id_billing_service)
                    })
                    sc.append((service_created.id, service_created.name))

            if line.entity_code not in partner_worked:
                if not Partner.search([('entity_code', '=', line.entity_code)]):
                    partner_created = Partner.create({
                        'name': line.entity_name,
                        'entity_name': line.entity_name,
                        'entity_code': line.entity_code,
                        'entity_type': line.entity_type,
                        'person_type': line.person_type,
                        'document_type': line.document_type,
                        'entity_address': line.entity_address,
                        'entity_district': line.entity_district,
                        'entity_province': line.entity_province,
                        'entity_country': line.entity_country,
                        'entity_collection': line.entity_collection,
                        'id_holder': line.id_holder,
                        'id_issuer': line.id_issuer,
                        'id_participant': line.id_participant,
                        'id_entity_block': line.id_entity_block
                    })
                    pc.append((partner_created.id, partner_created.name))
                    

            service_worked.append(line.id_billing_service)
            partner_worked.append(line.entity_code)
            
        self.state = 'validate'
        
    
    def action_done(self):
        Product = self.env['product.product']
        Partner = self.env['res.partner']
        Currency = self.env['res.currency']
        Invoice = self.env['account.move']
        
        group_data_line = groupby(self.line_ids, key=lambda l: l.id_billing_calculation)
        
        for group, lines in group_data_line:
            data = lines[0]
            currency_id = Currency.search([('name', '=', data.billing_currency)])
            invoice_data = {
                'partner_id': Partner.search([('entity_code', '=', data.entity_code)]).id,
                'invoice_date': data.billing_date,
                'currency_id': currency_id.id,
                'core_id': self.id,
                'process_date': data.process_date,
                'processed_state': data.processed_state,
                'billing_period': data.billing_period,
                'id_billing_calculation': data.id_billing_calculation,
                'payment_reference': data.payment_reference,
                'billing_date': data.billing_date,
                'billing_currency': data.billing_currency,           
                'ind_invoice_core': data.ind_invoice_core,
                'ind_web_service': data.ind_web_service,
                'ind_reject_core': data.ind_reject_core,
                'id_billing_detail': data.id_billing_detail,
                'type': 'out_invoice',
                'invoice_line_ids': [],
            }
            
            for line in lines:
                invoice_data['invoice_line_ids'].append((
                    0, 0, {
                        'product_id': Product.search([
                            ('id_billing_service', '=', line.id_billing_service)
                        ]).id,
                        'quantity': line.quantity,
                        'price_unit': line.service_rate,
                        
                    }
                ))
                
            Invoice.create(invoice_data)
            
        self.state = 'done'
    
    def button_invoices(self):
        action = {
            'name': 'Factura',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': [('core_id', '=', self.id)]
        }
        return action
        

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
