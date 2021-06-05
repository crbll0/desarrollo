# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.tools.misc import groupby
_logger = logging.getLogger(__name__)


class CuadreCaja(models.TransientModel):
    _name = 'wizard.cuadre.caja'
    _description = 'Wizard Cuadre de Caja'

    date_from = fields.Date(required=True)
    date_to = fields.Date(default=fields.Date.today(), required=True)
    
    user_ids = fields.Many2many('res.users')
    journal_ids = fields.Many2many('account.journal')
    
    def get_report(self):
        domain = [(1, '=', 1),
#             ('payment_date', '>=', date_from),
#             ('payment_date', '<=', date_to),
#             ('state', '!=', 'cancelled')
        ]
        
        if self.user_ids:
            domain.append(
                ('create_uid', 'in', self.user_ids.ids)
            )
            
        if self.journal_ids:
            domain.append(
                ('journal_id', 'in', self.journal_ids.ids)
            )

        payments = self.env['account.payment'].search(domain).ids

        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'journals': self.journal_ids.ids,
                'users': self.user_ids,
                'payments': payments,
            }
        }

        return self.env.ref('cuadre_caja.report_cuadre_caja').report_action(self, data=data)


class ReportSummaryReportView(models.AbstractModel):
    _name = 'report.cuadre_caja.report_cuadre_caja_view'
    _description = "Reporte Cuadre de Caja "
    
    def groupby_journal(self, payments):
        group = {}
        _logger.info(('payments>>>>>',payments))
        if payments:
            _logger.info(('payments>>>>>',payments))
            group = groupby(payments, key=lambda p: p.journal_id.id)
            _logger.info(('group>>>>>',group))
            
        return dict(group)
        
    def groupby_user(self, payments):
        group = {}
        if payments:
            group = groupby(payments, key=lambda p: p.create_uid)
        
        return dict(group)
        
    
    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        payment_ids = data['form']['payments']
        journal_ids = data['form']['journals']
        user_ids = data['form']['users']
        
        payments = self.env['account.payment'].browse(payment_ids)
        
        journals = [o.journal_id for o in payments]

        byjournal = self.groupby_journal(payments)
#         byuser = self.groupby_user(payments)
        
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_from': date_from,
            'date_to': date_to,
            'docs': data['ids'],
            'journals': set(journals),
            'byjournal': byjournal,
            'byuser': [],
        }