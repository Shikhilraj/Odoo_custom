# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError


class LeaveRequestReport(models.AbstractModel):
    _name = 'report.hostel_management.report_student_leave_request'
    _description = 'Leave Request Report'

    @api.model
    def _get_report_values(self, docids, data):
        """Get Report Values"""
        query = """
                    select st.name,rm.room_number,lr.leave_date,lr.arrival_date,
                    lr.duration from student_leave_request as lr inner join 
                    hostel_management_student_information as st on 
                    lr.student_id = st.id inner join 
                    hostel_management_room_management as rm on 
                    st.room_id = rm.id where 0=0 """
        if data['room']:
            query = query + f"""and rm.room_number='{data['room']}' """
        if data['student']:
            query = query + f"""and st.name='{data['student']}' """
        if data['start_date']:
            query = query + f"""and lr.leave_date >='{data['start_date']}' """
        if data['arrival_date']:
            query = query + f"""and lr.leave_date <='{data['arrival_date']}'"""

        self.env.cr.execute(query)
        result = self.env.cr.fetchall()
        if result:
            return {
                'data': data,
                'result': result
            }
        else:
            raise ValidationError('No Data Found')
