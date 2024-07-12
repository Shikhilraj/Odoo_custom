# -*- coding: utf-8 -*-
from odoo import fields, models


class HostelInvoice(models.Model):
    _inherit = 'account.move'

    student_id = fields.Many2one(
        'hostel.management.student.information', string='Student')

    def action_post(self):
        """Post the invoice and send mail to student in invoice"""
        super(HostelInvoice, self).action_post()
        if self.student_id.receive_mail:
            mail_template = (self.env.ref
                             ('hostel_management.hostel_rent_email_template'))
            mail_template.send_mail(self.id, force_send=True)
