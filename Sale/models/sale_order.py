from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """Credit Limit Warning"""
    _inherit = 'sale.order'

    due_amount = fields.Monetary(string='Due Amount',
                                 related='partner_id.due_amount')

    @api.onchange('partner_id')
    def onchange_credit_limit_warning(self):
        """Check whether the partner reaches the credit limit warning amount"""
        partner = self.partner_id
        new_balance = self.amount_total + partner.due_amount
        if new_balance > partner.credit_amount_warning > 0:
            res = {'warning': {
                'title': 'Warning',
                'message': 'The following customer is about or '
                           'exceeded their credit limit.'
            }}
            return res

    def action_confirm(self):
        """Override the action_post() method for check whether the customer
         reaches the credit limit block amount"""
        for order in self:
            partner = order.partner_id
            new_balance = order.amount_total + partner.due_amount
            if new_balance > partner.credit_amount_blocking > 0:
                raise ValidationError("Amount Exceeds the Blocking amount")
            return super(SaleOrder, self).action_confirm()

