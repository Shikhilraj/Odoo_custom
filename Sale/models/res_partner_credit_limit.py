from odoo import api, fields, models


class ResPartnerCreditLimit(models.Model):
    _inherit = 'res.partner'

    credit_limit_active = fields.Boolean(string='Active Credit Limit',
                                         default=False)
    credit_amount_warning = fields.Monetary(string='Warning Amount', default=0)
    credit_amount_blocking = fields.Monetary(string='Blocking Limit', default=0)
    due_amount = fields.Monetary(string='Due Amount', default=0,
                                 compute='_compute_due_amount', readonly=True)

    @api.depends('credit_limit_active')
    def _compute_due_amount(self):
        """Compute due amount of partner"""
        invoices = (self.env['account.move'].search
                    ([('partner_id', '=', self.name),
                      ('move_type', '=', 'out_invoice'),
                      ('state', 'not in', ['draft', 'cancel']),
                      ('payment_state', 'in', ['not_paid', 'partial'])
                      ]))
        total = 0
        for val in invoices:
            total = total + val.amount_total
        self.due_amount = total


