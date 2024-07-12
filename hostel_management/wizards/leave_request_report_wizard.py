# -*- coding: utf-8 -*-
import datetime
import io
import json
from odoo import fields, models
from odoo.tools import date_utils
from odoo.exceptions import ValidationError
import xlsxwriter


class LeaveRequestReportWizard(models.TransientModel):
    _name = 'leave.request.report.wizard'
    _description = 'Leave Request Report Wizard'

    room_id = fields.Many2one('hostel.management.room.management',
                              string='Room')
    student_id = fields.Many2one(
        'hostel.management.student.information', string='Student')
    start_date = fields.Date(string='Start Date')
    arrival_date = fields.Date(string='Arrival Date')
    # company_id = fields.Many2one('res.company',
    #                              default=lambda self: self.env.company)

    def action_leave_request_report(self):
        data = {
            'room': self.room_id.room_number,
            'student': self.student_id.name,
            'start_date': self.start_date,
            'arrival_date': self.arrival_date
        }
        return (self.env.ref('hostel_management.action_leave_request_report').
                report_action(self, data=data))

    def print_xlsx_report(self):
        data = {
            'room': self.room_id.room_number,
            'student': self.student_id.name,
            'start_date': self.start_date,
            'arrival_date': self.arrival_date
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'leave.request.report.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Student Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        query = """select st.name,rm.room_number,lr.leave_date,lr.arrival_date,
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
        result = self.env.cr.dictfetchall()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'right'})
        sub_value = (workbook.add_format
                     ({'font_size': '11px', 'bold': True, 'align': 'left'}))
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px',
             'bg_color': 'cyan'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        h3 = workbook.add_format(
            {'font_size': '11px', 'bold': True, 'align': 'center'})
        comp = workbook.add_format({'font_size': '10px', 'align': 'center',
                                    'bg_color': 'cyan'})
        th = ['SL.No', 'Name', 'Room', 'Start Date', 'Arrival Date', 'Duration']
        sheet.merge_range('A1:G3', 'STUDENTS LEAVE REQUEST REPORT', head)
        sheet.write('A4', 'Printed Date', cell_format)
        sheet.write('B4', str(datetime.date.today()), sub_value)
        sheet.merge_range('H1:I1', self.env.company.name, comp)
        sheet.merge_range('H2:I2', self.env.company.email, comp)
        sheet.merge_range('H3:I3', self.env.company.phone, comp)
        row = 4
        if data['student']:
            sheet.write(row, 0, 'Student:', cell_format)
            sheet.write(row, 1, data['student'], sub_value)
            row = row + 1
            th.remove('Name')
        if data['room']:
            sheet.write(row, 0, 'Room', cell_format)
            sheet.write(row, 1, data['room'], sub_value)
            row = row + 1
            th.remove('Room')
        if data['start_date']:
            sheet.write(row, 0, 'Start Date', cell_format)
            sheet.write(row, 1, data['start_date'], sub_value)
            row = row + 1
        if data['arrival_date']:
            sheet.write(row, 0, 'Arrival Date', cell_format)
            sheet.write(row, 1, data['arrival_date'], sub_value)
            row = row + 1
        row = row + 1
        for i in range(0, len(th)):
            sheet.write(row, i, th[i], h3)
        row = row + 1
        sheet.set_column(0, 7, 18)
        col = 0
        number = 1
        if result:
            for i in result:
                sheet.write(row, col, number, txt)
                for j in i:
                    if not data['student']:
                        sheet.write(row, col+1, i['name'], txt)
                        col = col+1
                    if not data['room']:
                        sheet.write(row, col+1, i['room_number'], txt)
                        col = col + 1
                    sheet.write(row, col+1, str(i['leave_date']), txt)
                    sheet.write(row, col+2, str(i['arrival_date']), txt)
                    sheet.write(row, col+3, str(i['duration']), txt)
                    break
                col = 0
                row = row + 1
                number = number + 1
        else:
            raise ValidationError("Data not found")
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
