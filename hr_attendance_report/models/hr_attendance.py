# -*- coding: utf-8 -*-
import datetime

from odoo import fields, models
import base64


class HrAttendance(models.Model):
    """"""
    _inherit = 'hr.attendance'
    _description = 'Hr Attendance'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)

    def action_day_wise_report_send(self):
        """Action for report attaching in to sending mail"""
        attendance_report = (
            self.env.ref('hr_attendance_report.action_report_hr_attendance'))
        data_record = base64.b64encode(
            self.env['ir.actions.report'].sudo()._render_qweb_pdf(
                attendance_report, [self.id], data=None)[0])
        ir_values = {
            'name': 'Day Wise Attendance ',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'hr.attendance',
        }
        attendance_report_attachment_id = self.env[
            'ir.attachment'].sudo().create(
            ir_values)
        if attendance_report_attachment_id:
            email_template = self.env.ref(
                'hr_attendance_report.day_wise_attendance_report_template')
            if email_template:
                email_values = {
                    'email_to': self.get_email_list(),
                    'email_cc': False,
                    'scheduled_date': False,
                    'recipient_ids': [],
                    'auto_delete': True,
                }
                email_template.attachment_ids = [
                    (fields.Command.link(attendance_report_attachment_id.id))]
                (email_template.with_context(date=datetime.date.today()).
                 send_mail(self.id, email_values=email_values, force_send=True))
                email_template.attachment_ids = [(fields.Command.clear())]

    def get_email_list(self):
        """Adding email partner email to email templates"""
        user = self.env.ref('hr_attendance.group_hr_attendance_manager').users
        email_list = [usr.partner_id.email for usr in user
                      if usr.partner_id.email]
        return ",".join(email_list)
