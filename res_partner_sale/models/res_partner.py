# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one('res.users', string='Customer',
                              default=lambda self: self.env.user)
    order_ids = fields.One2many('sale.order',
                                inverse_name='partner_id', string='Sale order')
    product_count = fields.Integer(compute='_compute_count')

    def _compute_count(self):
        """Invoice count"""
        for rec in self:
            rec.product_count = len(rec.order_ids.order_line.product_id)

    def get_invoices(self):
        """For getting student invoice."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Count',
            'view_type': 'tree,form',
            'view_mode': 'tree,form',
            'res_model': 'product.product',
            'domain': [('id', 'in', self.order_ids.order_line.product_id.ids)]
        }
