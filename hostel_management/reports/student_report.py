# -*- coding: utf-8 -*-
from odoo import api, models
from odoo.exceptions import ValidationError


class StudentFormReport(models.AbstractModel):
    _name = 'report.hostel_management.report_student'
    _description = 'Student Form Report'

    @api.model
    def _get_report_values(self, docids, data):
        """Get Report Values"""
        query = """select rm.room_number,st.pending_amount,st.name,
        st.payment_status from hostel_management_room_management as rm full 
        join hostel_management_student_information as st on 
        rm.id = st.room_id where 0=0 """
        if data['room']:
            query = query + f"""and rm.room_number='{data['room']}' """
        if data['student']:
            query = query + f"""and st.name = '{data['student']}' """
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        if result:
            return {
                'data': data,
                'result': result,
                'docs': self.env['hostel.management.student.information']
            }
        else:
            raise ValidationError("No record found")
