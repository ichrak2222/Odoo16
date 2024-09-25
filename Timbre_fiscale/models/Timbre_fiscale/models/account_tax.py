from odoo import fields, models, api


class AccountTax(models.Model):
    _inherit = "account.tax"
    timbre_fiscale = fields.Boolean(default=True, string="timbre fiscale")

