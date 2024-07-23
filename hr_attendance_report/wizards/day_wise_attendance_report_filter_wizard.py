# -*- coding: utf-8 -*-
from odoo import fields, models


class DayWiseAttendanceFilterWizard(models.TransientModel):
    _name = 'day.wise.attendance.report.filter.wizard'
    _description = 'Day Wise Attendance Report'

    date = fields.Date(string='Date', default=fields.Date.today())

    def action_day_wise_report(self):
        data = None
        if self.date:
            data = {'date': self.date}
        print("data", data)
        return (self.env.ref
                ('hr_attendance_report.action_report_hr_attendance').
                report_action(self, data=data))


