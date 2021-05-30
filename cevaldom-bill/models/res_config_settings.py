# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    core_host = fields.Char(string="Host")
    core_port = fields.Char(string="Port")
    core_user = fields.Char(string="User")
    core_pass = fields.Char(string="Password")
    core_db = fields.Char(string="Database Name")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    core_host = fields.Char(relate='company_id.core_host', readonly=False)
    core_port = fields.Char(relate='company_id.core_port', readonly=False)
    core_user = fields.Char(relate='company_id.core_user', readonly=False)
    core_pass = fields.Char(relate='company_id.core_pass', readonly=False)
    core_db = fields.Char(relate='company_id.core_db', readonly=False)

