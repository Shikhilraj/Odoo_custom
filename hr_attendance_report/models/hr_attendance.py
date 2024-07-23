# -*- coding: utf-8 -*-
from odoo import api, fields, models
import base64


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    manager_email = fields.Char(default=lambda self: self.env.user.email)

    def action_day_wise_report_send(self):
        print('Mail sending')
        desired_group_name = self.env['res.groups'].search_read(
            [('name', '=', 'Administrator')])
        admin = self.env['res.users'].has_group('hr_attendance.group_hr_attendance_manager')
        print('Admin :', admin)


        # mail_template = (
        #     self.env.ref
        #     ('hr_attendance_report.day_wise_attendance_report_template'))
        # mail_template.send_mail(self.id, force_send=True)

        print("mail success : ", self.manager_email)
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
            'res_model': 'account.move',
        }
        attendance_report_attachment_id = self.env[
            'ir.attachment'].sudo().create(
            ir_values)
        if attendance_report_attachment_id:
            email_template = self.env.ref(
                'hr_attendance_report.day_wise_attendance_report_template')
        email = self.env['res.users'].search_read(['has_group', '=', 'group_hr_attendance_manager'])
        print("email : ", email)
