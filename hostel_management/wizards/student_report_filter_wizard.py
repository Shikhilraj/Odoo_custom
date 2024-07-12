# -*- coding: utf-8 -*-
import datetime
import io
import json
import xlsxwriter
from odoo import fields, models
from odoo.tools import date_utils
from odoo.exceptions import ValidationError


class StudentReportFilterWizard(models.TransientModel):
    _name = 'student.report.filter.wizard'
    _description = 'Student Report Filter Wizard'

    room_id = fields.Many2one('hostel.management.room.management',
                              string='Room')
    student_id = fields.Many2one(
        'hostel.management.student.information', string='Student')

    def print_student_report(self):
        data = {'room': self.room_id.room_number,
                'student': self.student_id.name}
        return (self.env.ref('hostel_management.action_report_student').
                report_action(self, data=data))

    def print_xlsx_report(self):
        data = {
            'model_id': self.id,
            'student': self.student_id.name,
            'room': self.room_id.room_number
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'student.report.filter.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Student Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        query = """select rm.room_number,st.pending_amount,st.name,
                       st.payment_status from hostel_management_room_management 
                       as rm full join hostel_management_student_information 
                       as st on rm.id = st.room_id where 0=0 """
        if data['room']:
            query = query + f""" and rm.room_number='{data['room']}' """
        if data['student']:
            query = query + f"""and st.name = '{data['student']}' """
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'right'})
        sub_val = workbook.add_format(
            {'font_size': '11px', 'bold': True, 'align': 'left'})
        h3 = workbook.add_format(
            {'font_size': '11px', 'bold': True, 'align': 'center'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px',
             'bg_color': 'cyan'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        comp = workbook.add_format({'font_size': '10px', 'align': 'center',
                                    'bg_color': 'cyan'})
        th = ['SL.No', 'Name', 'Pending Amount', 'Room', 'Invoice status']
        sheet.merge_range('A1:G3', 'STUDENT REPORT', head)
        sheet.write('A4', 'Printed Date', cell_format)
        sheet.write('B4', str(datetime.date.today()), sub_val)
        sheet.merge_range('H1:I1', self.env.company.name, comp)
        sheet.merge_range('H2:I2', self.env.company.email, comp)
        sheet.merge_range('H3:I3', self.env.company.phone, comp)
        row = 6
        if data['student']:
            sheet.write('A5', 'Student:', cell_format)
            sheet.write('B5', data['student'], sub_val)
            th.remove('Name')
            if data['room']:
                sheet.write('A6', 'Room', cell_format)
                sheet.write('B6', data['room'], sub_val)
                th.remove('Room')
                row = row + 1
        else:
            if data['room']:
                sheet.write('A5', 'Room', cell_format)
                sheet.write('B5', data['room'], sub_val)
                th.remove('Room')
        sheet.set_column(0, 7, 18)

        # Table head

        for i in range(0, len(th)):
            sheet.write(row, i, th[i], h3)
        row = row + 1
        """Table Body
        """

        col = 0
        number = 1
        if result:
            for i in result:
                sheet.write(row, col, number, txt)
                for j in i:
                    if not data['student']:
                        sheet.write(row, col + 1, i['name'], txt)
                        col = col + 1
                    sheet.write(row, col + 1, i['pending_amount'], txt)
                    if not data['room']:
                        sheet.write(row, col + 2, i['room_number'], txt)
                        col = col + 1
                    sheet.write(
                        row, col + 2,
                        dict(self.env['hostel.management.student.information']
                             ._fields['payment_status'].selection).
                        get(i['payment_status']), txt)
                    break
                col = 0
                row = row + 1
                number = number + 1
        else:
            raise ValidationError("No data Found")

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
