# -*- coding: utf-8 -*-

from odoo import models, fields, api


class BillResPartner(models.Model):
    _inherit = 'res.partner'

    entity_code = fields.Char(string="ENTITY CODE")
    person_type = fields.Selection([
        ('NATURAL', 'NATURAL'),
        ('JURIDICO', 'JURIDICO')
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
