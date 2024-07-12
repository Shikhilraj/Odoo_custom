# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Facilities(models.Model):
    _name = 'hostel.management.facilities'
    _description = 'Facilities'
    _inherit = 'mail.thread'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    charge = fields.Float(string='Charge')
    currency_id = fields.Many2one('res.currency',
                                  string='Currency', required=True,
                                  default=lambda self:
                                  self.env.user.company_id.currency_id)

    @api.constrains('charge')
    def check_charge(self):
        """ Check the field charge whether value is 0 or not."""
        if self.charge <= 0:
            raise ValidationError("Check charge field")
