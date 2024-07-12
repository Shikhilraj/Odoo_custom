# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    """Product template for add sale count field"""
    _inherit = 'product.template'

    sale_count = fields.Integer(string='Sale Count', compute='_compute_count')

    def _compute_count(self):
        """Invoice count"""
        for rec in self:
            rec.sale_count = (rec.env['sale.order.line'].
                              search_count([('product_id', '=', self.id)]))
            print(rec.sale_count)
