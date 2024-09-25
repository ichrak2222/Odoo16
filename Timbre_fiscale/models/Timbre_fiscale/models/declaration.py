from odoo import fields, models, api


class ModelName(models.Model):
    _name = 'declaration'
    _description = 'Description'

    name = fields.Char(string="declaration")
