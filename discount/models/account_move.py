# Copyright 2019 Tecnativa - David Vidal
# Copyright 2020 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
from odoo import _, api, exceptions, fields, models
from odoo.tools import config

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    base_before_global_discounts = fields.Monetary(
        string="Amount Untaxed Before Discounts", readonly=True,
    )
    global_discount_item = fields.Boolean()

   
    def _get_global_discount_vals(self, base, **kwargs):
        """ Prepare the dict of values to create to obtain the discounted
            amount
           :param float base: the amount to discount
           :return: dict with the discounted amount
        """
        self.ensure_one()
        
        account_id = self.env['account.account'].search([
            ('discount', '=', True), 
#             ('company_id', '=', self.env.user.company.id)
        ], limit=1).id
        
        return {
            "base": base,
            "account_id": account_id,
            "base_discounted": base * (1 - (self.discount / 100)),
        }
    
    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
        ''' This method is used to compute 'price_total' & 'price_subtotal'.
        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # Compute 'price_subtotal'.
        price_unit_wo_discount = price_unit #* (1 - (discount / 100.0))
        subtotal = quantity * price_unit_wo_discount

        # Compute 'price_total'.
        if taxes:
            force_sign = -1 if move_type in ('out_invoice', 'in_refund', 'out_receipt') else 1
            taxes_res = taxes._origin.with_context(force_sign=force_sign).compute_all(price_unit_wo_discount,
                quantity=quantity, currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        #In case of multi currency, round before it's use for computing debit credit
        if currency:
            res = {k: currency.round(v) for k, v in res.items()}
        return res



class AccountMove(models.Model):
    _inherit = "account.move"
    

    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        ''' Compute the dynamic tax lines of the journal entry.
        :param lines_map: The line_ids dispatched by type containing:
            * base_lines: The lines having a tax_ids set.
            * tax_lines: The lines having a tax_line_id set.
            * terms_lines: The lines generated by the payment terms of the invoice.
            * rounding_lines: The cash rounding lines of the invoice.
        '''
        self.ensure_one()
        in_draft_mode = self != self._origin

        def _serialize_tax_grouping_key(grouping_dict):
            ''' Serialize the dictionary values to be used in the taxes_map.
            :param grouping_dict: The values returned by '_get_tax_grouping_key_from_tax_line' or '_get_tax_grouping_key_from_base_line'.
            :return: A string representing the values.
            '''
            return '-'.join(str(v) for v in grouping_dict.values())

        def _compute_base_line_taxes(base_line):
            ''' Compute taxes amounts both in company currency / foreign currency as the ratio between
            amount_currency & balance could not be the same as the expected currency rate.
            The 'amount_currency' value will be set on compute_all(...)['taxes'] in multi-currency.
            :param base_line:   The account.move.line owning the taxes.
            :return:            The result of the compute_all method.
            '''
            move = base_line.move_id

            if move.is_invoice(include_receipts=True):
                handle_price_include = True
                sign = -1 if move.is_inbound() else 1
                quantity = base_line.quantity
                if base_line.currency_id:
                    price_unit_foreign_curr = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
                    price_unit_comp_curr = base_line.currency_id._convert(price_unit_foreign_curr, move.company_id.currency_id, move.company_id, move.date, round=False)
                else:
                    price_unit_foreign_curr = 0.0
                    price_unit_comp_curr = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
                tax_type = 'sale' if move.type.startswith('out_') else 'purchase'
                is_refund = move.type in ('out_refund', 'in_refund')
            else:
                handle_price_include = False
                quantity = 1.0
                price_unit_foreign_curr = base_line.amount_currency
                price_unit_comp_curr = base_line.balance
                tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
                is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)

            balance_taxes_res = base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
                price_unit_comp_curr,
                currency=base_line.company_currency_id,
                quantity=quantity,
                product=base_line.product_id,
                partner=base_line.partner_id,
                is_refund=is_refund,
                handle_price_include=handle_price_include,
            )

            if move.type == 'entry':
                repartition_field = is_refund and 'refund_repartition_line_ids' or 'invoice_repartition_line_ids'
                repartition_tags = base_line.tax_ids.flatten_taxes_hierarchy().mapped(repartition_field).filtered(lambda x: x.repartition_type == 'base').tag_ids
                tags_need_inversion = (tax_type == 'sale' and not is_refund) or (tax_type == 'purchase' and is_refund)
                if tags_need_inversion:
                    balance_taxes_res['base_tags'] = base_line._revert_signed_tags(repartition_tags).ids
                    for tax_res in balance_taxes_res['taxes']:
                        tax_res['tag_ids'] = base_line._revert_signed_tags(self.env['account.account.tag'].browse(tax_res['tag_ids'])).ids

            if base_line.currency_id:
                # Multi-currencies mode: Taxes are computed both in company's currency / foreign currency.
                amount_currency_taxes_res = base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
                    price_unit_foreign_curr,
                    currency=base_line.currency_id,
                    quantity=quantity,
                    product=base_line.product_id,
                    partner=base_line.partner_id,
                    is_refund=self.type in ('out_refund', 'in_refund'),
                    handle_price_include=handle_price_include,
                )

                if move.type == 'entry':
                    repartition_field = is_refund and 'refund_repartition_line_ids' or 'invoice_repartition_line_ids'
                    repartition_tags = base_line.tax_ids.mapped(repartition_field).filtered(lambda x: x.repartition_type == 'base').tag_ids
                    tags_need_inversion = (tax_type == 'sale' and not is_refund) or (tax_type == 'purchase' and is_refund)
                    if tags_need_inversion:
                        balance_taxes_res['base_tags'] = base_line._revert_signed_tags(repartition_tags).ids
                        for tax_res in balance_taxes_res['taxes']:
                            tax_res['tag_ids'] = base_line._revert_signed_tags(self.env['account.account.tag'].browse(tax_res['tag_ids'])).ids

                for b_tax_res, ac_tax_res in zip(balance_taxes_res['taxes'], amount_currency_taxes_res['taxes']):
                    tax = self.env['account.tax'].browse(b_tax_res['id'])
                    b_tax_res['amount_currency'] = ac_tax_res['amount']

                    # A tax having a fixed amount must be converted into the company currency when dealing with a
                    # foreign currency.
                    if tax.amount_type == 'fixed':
                        b_tax_res['amount'] = base_line.currency_id._convert(b_tax_res['amount'], move.company_id.currency_id, move.company_id, move.date)

            return balance_taxes_res

        taxes_map = {}

        # ==== Add tax lines ====
        to_remove = self.env['account.move.line']
        for line in self.line_ids.filtered('tax_repartition_line_id'):
            grouping_dict = self._get_tax_grouping_key_from_tax_line(line)
            grouping_key = _serialize_tax_grouping_key(grouping_dict)
            if grouping_key in taxes_map:
                # A line with the same key does already exist, we only need one
                # to modify it; we have to drop this one.
                to_remove += line
            else:
                taxes_map[grouping_key] = {
                    'tax_line': line,
                    'balance': 0.0,
                    'amount_currency': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                }
        if not recompute_tax_base_amount:
            self.line_ids -= to_remove

        # ==== Mount base lines ====
        for line in self.line_ids.filtered(lambda line: not line.tax_repartition_line_id):
            # Don't call compute_all if there is no tax.
            if not line.tax_ids:
                if not recompute_tax_base_amount:
                    line.tag_ids = [(5, 0, 0)]
                continue

            compute_all_vals = _compute_base_line_taxes(line)

            # Assign tags on base line
            if not recompute_tax_base_amount:
                line.tag_ids = compute_all_vals['base_tags'] or [(5, 0, 0)]

            tax_exigible = True
            for tax_vals in compute_all_vals['taxes']:
                grouping_dict = self._get_tax_grouping_key_from_base_line(line, tax_vals)
                grouping_key = _serialize_tax_grouping_key(grouping_dict)

                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_vals['tax_repartition_line_id'])
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id

                if tax.tax_exigibility == 'on_payment':
                    tax_exigible = False

                taxes_map_entry = taxes_map.setdefault(grouping_key, {
                    'tax_line': None,
                    'balance': 0.0,
                    'amount_currency': 0.0,
                    'tax_base_amount': 0.0,
                    'grouping_dict': False,
                })
                taxes_map_entry['balance'] += tax_vals['amount']
                taxes_map_entry['amount_currency'] += tax_vals.get('amount_currency', 0.0)
                taxes_map_entry['tax_base_amount'] += self._get_base_amount_to_display(tax_vals['base'], tax_repartition_line, tax_vals['group'])
                taxes_map_entry['grouping_dict'] = grouping_dict
            if not recompute_tax_base_amount:
                line.tax_exigible = tax_exigible

        # ==== Process taxes_map ====
        for taxes_map_entry in taxes_map.values():
            # Don't create tax lines with zero balance.
            if self.currency_id.is_zero(taxes_map_entry['balance']) and self.currency_id.is_zero(taxes_map_entry['amount_currency']):
                taxes_map_entry['grouping_dict'] = False

            tax_line = taxes_map_entry['tax_line']

            if not tax_line and not taxes_map_entry['grouping_dict']:
                continue
            elif tax_line and recompute_tax_base_amount:
                tax_line.tax_base_amount = taxes_map_entry['tax_base_amount']
            elif tax_line and not taxes_map_entry['grouping_dict']:
                # The tax line is no longer used, drop it.
                self.line_ids -= tax_line
            elif tax_line:
                tax_line.update({
                    'amount_currency': taxes_map_entry['amount_currency'],
                    'debit': taxes_map_entry['balance'] > 0.0 and taxes_map_entry['balance'] or 0.0,
                    'credit': taxes_map_entry['balance'] < 0.0 and -taxes_map_entry['balance'] or 0.0,
                    'tax_base_amount': taxes_map_entry['tax_base_amount'],
                })
            elif not recompute_tax_base_amount:
                create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
                tax_repartition_line_id = taxes_map_entry['grouping_dict']['tax_repartition_line_id']
                tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_repartition_line_id)
                tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id
                tax_line = create_method({
                    'name': tax.name,
                    'move_id': self.id,
                    'partner_id': line.partner_id.id,
                    'company_id': line.company_id.id,
                    'company_currency_id': line.company_currency_id.id,
                    'quantity': 1.0,
                    'date_maturity': False,
                    'amount_currency': taxes_map_entry['amount_currency'],
                    'debit': taxes_map_entry['balance'] > 0.0 and taxes_map_entry['balance'] or 0.0,
                    'credit': taxes_map_entry['balance'] < 0.0 and -taxes_map_entry['balance'] or 0.0,
                    'tax_base_amount': taxes_map_entry['tax_base_amount'],
                    'exclude_from_invoice_tab': True,
                    'tax_exigible': tax.tax_exigibility == 'on_invoice',
                    **taxes_map_entry['grouping_dict'],
                })

            if tax_line and in_draft_mode:
                tax_line._onchange_amount_currency()
                tax_line._onchange_balance()

    amount_global_discount = fields.Monetary(
        string="Total Global Discounts",
        compute="_compute_amount",
        currency_field="currency_id",
        readonly=True,
        compute_sudo=True,
    )
    amount_untaxed_before_global_discounts = fields.Monetary(
        string="Amount Untaxed Before Discounts",
        compute="_compute_amount",
        currency_field="currency_id",
        readonly=True,
        compute_sudo=True,
    )
    invoice_global_discount_ids = fields.One2many(
        comodel_name="account.invoice.global.discount",
        inverse_name="invoice_id",
        readonly=True,
    )

    def _recompute_tax_lines(self, recompute_tax_base_amount=False):
        super()._recompute_tax_lines(recompute_tax_base_amount)
        # If recompute_tax_base_amount is True, only the tax_base_amount
        # field is recalculated, therefore the debit and debit fields
        # will not be recalculated and it doesn't make sense to apply
        # the global discount to the taxes move lines by calling the
        # _update_tax_lines_for_global_discount method.
        if not recompute_tax_base_amount:
            self._update_tax_lines_for_global_discount()

    def _update_tax_lines_for_global_discount(self):
        """ Update tax_base_amount and taxes debits."""
        round_curr = self.currency_id.round
        tax_lines = self.line_ids.filtered(
            lambda r: r.tax_line_id.amount_type in ("percent", "division")
        )
        for tax_line in tax_lines:
            base = tax_line.tax_base_amount
            tax_line.base_before_global_discounts = base
            amount = tax_line.balance
            for discount in self.global_discount_ids():
                base = tax_line._get_global_discount_vals(base)["base_discounted"]
                amount = tax_line._get_global_discount_vals(amount)["base_discounted"]
                
            tax_line.tax_base_amount = round_curr(base)
            tax_line.debit = amount > 0.0 and amount or 0.0
            tax_line.credit = amount < 0.0 and -amount or 0.0
            
            # Apply onchanges
            tax_line._onchange_amount_currency()
            tax_line._onchange_balance()

    def _prepare_global_discount_vals(self, global_discount, base, tax_ids):
        """Prepare the dictionary values for an invoice global discount
        line.
        """
        account_id = self.env['account.account'].search([
            ('discount', '=', True), 
#             ('company_id', '=', self.env.user.company.id)
        ], limit=1).id
        lines = self._context.get('lines')
        base = 0
        for l in lines:
            base += l.price_unit * l.quantity
            discount = l._get_global_discount_vals(base)
        
        return {
            "name": 'Descuento', # global_discount.display_name,
            "invoice_id": self.id,
            "discount": global_discount,
            "base": base,
            "base_discounted": discount["base_discounted"],
            "account_id":account_id,
            "tax_ids": [(4, tax_id) for tax_id in tax_ids],
        }
    
    def global_discount_ids(self):
        discount = {}
        for l in self.invoice_line_ids:
            discount.setdefault(l.discount, self.env['account.move.line'])
            discount[l.discount] += l
        return discount

    def _set_global_discounts_by_tax(self):
        pass
        """Create invoice global discount lines by taxes combinations and
        discounts.
        """
        self.ensure_one()
        taxes_keys = {}
        # Perform a sanity check for discarding cases that will lead to
        # incorrect data in discounts
        for inv_line in self.invoice_line_ids.filtered(lambda l: not l.display_type):
            if not inv_line.tax_ids and (
                not config["test_enable"]
                or self.env.context.get("test_account_global_discount")
            ):
                raise exceptions.UserError(
                    _("With global discounts, taxes in lines are required.")
                )
            for key in taxes_keys:
                if key == tuple(inv_line.tax_ids.ids):
                    break
                elif set(key) & set(inv_line.tax_ids.ids) and (
                    not config["test_enable"]
                    or self.env.context.get("test_account_global_discount")
                ):
                    raise exceptions.UserError(
                        _("Incompatible taxes found for global discounts.")
                    )
            else:
                taxes_keys[tuple(inv_line.tax_ids.ids)] = True
        self.invoice_global_discount_ids.unlink()# = False
        invoice_global_discounts = []
        for tax_line in self.line_ids.filtered("tax_line_id"):
            key = []
            to_create = True
            for key in taxes_keys:
                if tax_line.tax_line_id.id in key:
                    to_create = taxes_keys[key]
                    taxes_keys[key] = False  # mark for not duplicating
                    break  # we leave in key variable the proper taxes value
            if not to_create:
                continue
            base = tax_line.base_before_global_discounts or tax_line.tax_base_amount
            for global_discount, lines in self.global_discount_ids().items():
                vals = self.with_context({'lines': lines})._prepare_global_discount_vals(global_discount, base, key)
                invoice_global_discounts.append((0, 0, vals))
                base = vals["base_discounted"]
        # Check all moves with defined taxes to check if there's any discount not
        # created (tax amount is zero and only one tax is applied)
        for line in self.line_ids.filtered("tax_ids"):
            key = tuple(line.tax_ids.ids)
            if taxes_keys.get(key):
                base = line.price_subtotal
                for global_discount, lines in self.global_discount_ids().items():
                    vals = self.with_context({'lines': lines})._prepare_global_discount_vals(
                        global_discount, base, key
                    )
                    invoice_global_discounts.append((0, 0, vals))
                    base = vals["base_discounted"]
        self.invoice_global_discount_ids = invoice_global_discounts

    def _create_global_discount_journal_items(self):
        """Append global discounts move lines"""
        lines_to_delete = self.line_ids.filtered("global_discount_item")
#         lines_to_delete = self.line_ids.filtered(lambda l: l.discount > 0.00)
        if self != self._origin:
            self.line_ids -= lines_to_delete
        else:
            lines_to_delete.with_context(check_move_validity=False).unlink()
            
        account_id = self.env['account.account'].search([
            ('discount', '=', True)
        ], limit=1)
            
        vals_list = []
        for discount in self.invoice_global_discount_ids.filtered("discount"):
            disc_amount = discount.discount_amount
            vals_list.append(
                (
                    0, 0,
                    {
                        "global_discount_item": True,
                        "name": "Descuento del {}% - {}".format(
                            discount.discount, ", ".join(discount.tax_ids.mapped("name"))),
                        "debit": disc_amount > 0.0 and disc_amount or 0.0,
                        "credit": disc_amount < 0.0 and -disc_amount or 0.0,
                        "account_id": account_id.id,
#                         "analytic_account_id": discount.account_analytic_id.id,
                        "exclude_from_invoice_tab": True,
                    },
                )
            )
        self.line_ids = vals_list
        self._onchange_recompute_dynamic_lines()

    def _set_global_discounts(self):
        """Get global discounts in order and apply them in chain. They will be
        fetched in their sequence order"""
        for inv in self:
            inv._set_global_discounts_by_tax()
            inv._create_global_discount_journal_items()

    @api.onchange("invoice_line_ids")
    def _onchange_invoice_line_ids(self):
        others_lines = self.line_ids.filtered(
            lambda line: line.exclude_from_invoice_tab
        )
        if others_lines:
            others_lines[0].recompute_tax_line = True
        res = super()._onchange_invoice_line_ids()
        self._set_global_discounts()
        return res

    def _compute_amount_one(self):
        if not self.invoice_global_discount_ids:
            self.amount_global_discount = 0.0
            self.amount_untaxed_before_global_discounts = 0.0
            return
        
        round_curr = self.currency_id.round
        self.amount_global_discount = sum(
            round_curr(discount.discount_amount) * -1
            for discount in self.invoice_global_discount_ids
        )
        self.amount_untaxed_before_global_discounts = self.amount_untaxed
        self.amount_untaxed = self.amount_untaxed + self.amount_global_discount
        self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if (
            self.currency_id
            and self.company_id
            and self.currency_id != self.company_id.currency_id
        ):
            date = self.invoice_date or fields.Date.today()
            amount_total_company_signed = self.currency_id._convert(
                self.amount_total, self.company_id.currency_id, self.company_id, date
            )
            amount_untaxed_signed = self.currency_id._convert(
                self.amount_untaxed, self.company_id.currency_id, self.company_id, date
            )
        sign = self.type in ["in_refund", "out_refund"] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    @api.depends(
        "line_ids.debit",
        "line_ids.credit",
        "line_ids.currency_id",
        "line_ids.amount_currency",
        "line_ids.amount_residual",
        "line_ids.amount_residual_currency",
        "line_ids.payment_id.state",
        "invoice_global_discount_ids",
#         "invoice_line_ids",
#         "global_discount_ids",
    )
    def _compute_amount(self):
        super()._compute_amount()
        for record in self:
            record._set_global_discounts()
            record._compute_amount_one()



class AccountInvoiceGlobalDiscount(models.Model):
    _name = "account.invoice.global.discount"
    _description = "Invoice Global Discount"

    name = fields.Char(string="Discount Name", required=True)
    invoice_id = fields.Many2one(
        "account.move",
        string="Invoice",
        ondelete="cascade",
        index=True,
        readonly=True,
        domain=[
            ("type", "in", ["out_invoice", "out_refund", "in_invoice", "in_refund"])
        ],
    )
#     global_discount_id = fields.Many2one(
#         comodel_name="global.discount", string="Global Discount", readonly=True,
#     )
    discount = fields.Float(string="Discount (number)", readonly=True)
    discount_display = fields.Char(
        compute="_compute_discount_display", readonly=True, string="Discount",
    )
    base = fields.Float(
        string="Base discounted", digits="Product Price", readonly=True,
    )
    base_discounted = fields.Float(
        string="Discounted amount", digits="Product Price", readonly=True,
    )
    currency_id = fields.Many2one(related="invoice_id.currency_id", readonly=True)
    discount_amount = fields.Monetary(
        string="Discounted Amount",
        compute="_compute_discount_amount",
        currency_field="currency_id",
        readonly=True,
        compute_sudo=True,
    )
    tax_ids = fields.Many2many(comodel_name="account.tax")
    account_id = fields.Many2one(
        comodel_name="account.account",
        required=True,
        string="Account",
        domain="[('user_type_id.type', 'not in', ['receivable', 'payable'])]",
    )
    account_analytic_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Analytic account",
    )
    company_id = fields.Many2one(related="invoice_id.company_id", readonly=True)

    def _compute_discount_display(self):
        """Given a discount type, we need to render a different symbol"""
        for one in self:
            precision = self.env["decimal.precision"].precision_get("Discount")
            one.discount_display = "{0:.{1}f}%".format(one.discount * -1, precision)

    @api.depends("base", "base_discounted")
    def _compute_discount_amount(self):
        """Compute the amount discounted"""
        for one in self:
            one.discount_amount = one.base - one.base_discounted


class AccountAccount(models.Model):
    _inherit = 'account.account'
    
    discount = fields.Boolean('Para Descuento')
    