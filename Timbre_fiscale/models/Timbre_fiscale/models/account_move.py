import self as self

from odoo import fields, models, api
from odoo.addons.website_sale_digital.models.account_invoice import AccountInvoiceLine
from odoo.exceptions import UserError
from odoo.tests import Form


class AccountMove(models.Model):
    _inherit = 'account.move'


    timbre = fields.Monetary(string="Timbre", compute="_compute_timbre_fiscale", store=True)

    @api.depends("partner_id", "partner_id.timbre_fiscale")
    def _compute_timbre_fiscale(self):
        for record in self:
            record.timbre = 1.0 if record.partner_id.timbre_fiscale else 0

'''

    @api.depends(
        "line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched",
        "line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual",
        "line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency",
        "line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched",
        "line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual",
        "line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency",
        "line_ids.balance",
        "line_ids.currency_id",
        "line_ids.amount_currency",
        "line_ids.amount_residual",
        "line_ids.amount_residual_currency",
        "line_ids.payment_id.state",
        "line_ids.full_reconcile_id",
    )



    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()
        for move in self:
            if move.partner_id.timbre_fiscale:
                # self.env: rechercher un champ qui se trouve dans un autre modéle
                tax_id = self.env["account.tax"].search(
                    [("timbre_fiscale", "=", True), ("type_tax_use", "=", "sale")],
                    limit=1,
                )
                amount = tax_id.amount
                move.amount_untaxed += amount
                move.amount_total += amount
                move.amount_residual += amount
                move.amount_untaxed_signed += amount
                move.amount_total_signed += amount
                move.amount_residual_signed += amount
                move.amount_total_in_currency_signed += amount
                # Add a new line to balance the move
               
                if move.amount_total > 0:
                    account_id = move.journal_id.default_credit_account_id.id
                    if not account_id:
                        raise UserError("Please specify a default credit account on the journal.")
                    self.env['account.move.line'].create({
                        'move_id': move.id,
                        'name': 'Balance line',
                        'account_id': account_id,
                        'debit': 0.0,
                        'credit': move.amount_total - amount,
                    })
                 
                elif move.amount_total < 0:
                    account_id = move.journal_id.default_debit_account_id.id
                    if not account_id:
                        raise UserError("Please specify a default debit account on the journal.")
                    self.env['account.move.line'].create({
                        'move_id': move.id,
                        'name': 'Balance line',
                        'account_id': account_id,
                        'debit': - move.amount_total - amount,
                        'credit': 0.0,
                    })
                    

                # Update the move's amounts
                move.amount_untaxed += amount
                move.amount_total += amount
                move.amount_residual += amount
                move.amount_untaxed_signed += amount
                move.amount_total_signed += amount
                move.amount_residual_signed += amount
                move.amount_total_in_currency_signed += amount


        return res



class Journal(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def add_tax_to_journal(self):
        # Récupérez l'ID de la taxe "timbre fiscale"
        tax_id = self.env['account.move.line'].search([('name', '=', 'Timbre fiscale')]).id

        # Récupérez l'ID du journal dans lequel vous souhaitez ajouter la taxe
        journal_id = self.env['account.move.line'].search([('code', '=', 'VENT')]).id

        # Ajoutez la taxe au journal
        journal = self.env['account.move.line'].browse(account_id)
        if tax_id not in account_id.name:
            journal.write({'name': [(4, tax_id)]})
            '''
'''
from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    stamp_duty_account_id = fields.Many2one('account.account', string='Stamp Duty Account')

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def create(self, vals):
        if 'journal_id' in vals:
            journal = self.env['account.journal'].browse(vals['journal_id'])
            if journal.stamp_duty_account_id:
                stamp_duty = journal.stamp_duty_account_id.get_balance(vals['company_id'], vals['currency_id'])
                vals['debit'] += stamp_duty
        return super().create(vals)
'''
