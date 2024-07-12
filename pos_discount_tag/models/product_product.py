# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    discount_prize = fields.Monetary(string='Discount Prize', default=0)
