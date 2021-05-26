# -*- coding: utf-8 -*-

from odoo import models, fields, api



class ResConfigSettings(models.TransientModel):
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
