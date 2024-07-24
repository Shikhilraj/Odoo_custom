# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DayWiseAttendanceReport(models.AbstractModel):
    _name = 'report.hr_attendance_report.report_day_wise_attendance'
    _description = 'Day Wise Attendance Report'

    @api.model
    def _get_report_values(self, docids, data):
        """Get Report Values"""
        query = f""" select emp.name,emp.work_email,att.check_in,att.check_out, 
        att.in_mode,emp.job_title from hr_attendance as att inner join 
        hr_employee as emp on att.employee_id = emp.id where 
        att.check_in >='{fields.Date.today()} 00:00:00' and 
        att.check_in <= '{fields.Date.today()} 23:59:59' """
        self.env.cr.execute(query)
        result = self.env.cr.fetchall()
        if result:
            return {
                'data': data,
                'result': result,
            }
        else:
            return False
