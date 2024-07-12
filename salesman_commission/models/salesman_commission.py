# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SalesmanCommission(models.Model):
    """Class for Salesman Commission"""
    _name = 'salesman.commission'
    _description = 'Salesman Commission'
    _rec_name = 'user_id'
    _inherit = ['mail.thread']

    user_id = fields.Many2one('res.users', string='Name')
    sales_value = fields.Monetary(string='Sales Value', default=0,
                                  compute='_compute_sales_value')
    percent = fields.Float(string='Percent', readonly=False)
    commission = fields.Monetary(string='Commission', default=0, tracking=True,
                                 compute='_compute_calculate_commission')
    preparer_id = fields.Many2one('res.users', string='Prepared By',
                                  tracking=True, readonly=True)
    approver_id = fields.Many2one('res.users', string='Approved By',
                                  tracking=True, readonly=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self:
                                 self.env.user.company_id.id,
                                 readonly=True)
    currency_id = fields.Many2one(related='company_id.currency_id',
                                  string='Currency', readonly=True)
    state = fields.Selection(string='State', default='new',
                             selection=[('new', 'New'),
                                        ('prepared', 'Prepare'),
                                        ('approved', 'Approved')])

    @api.depends('user_id')
    def _compute_sales_value(self):
        """Compute sales value of sales person"""
        total = 0
        for val in self:
            for rec in val.env['account.move'].search([('user_id', '=',
                                                        val.user_id.id)]):
                total = total + rec.amount_total
            self.sales_value = total

    @api.depends('sales_value', 'percent')
    def _compute_calculate_commission(self):
        """Calculate the commission amount of sales person."""
        for rec in self:
            rec.commission = rec.sales_value * (rec.percent/100)

    def action_prepare(self):
        """Method for prepare the commission."""
        self.preparer_id = self.env.user.id
        self.write({'state': 'prepared'})

    def action_approve(self):
        """Method for Approve the commission."""
        self.approver_id = self.env.user.id
        self.write({'state': 'approved'})
