from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    timbre_fiscale = fields.Boolean(string="timbre fiscale",default=False)
