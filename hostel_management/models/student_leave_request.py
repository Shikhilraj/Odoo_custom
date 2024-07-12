# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class LeaveRequest(models.Model):
    _name = 'student.leave.request'
    _description = 'Leave Request'
    _inherit = 'mail.thread'
    _rec_name = 'leave_date'

    leave_date = fields.Datetime(required=True, string='Leave Date',
                                 default=datetime.today())
    arrival_date = fields.Datetime(required=True, string='Arrival Date',
                                   default=datetime.today())
    state = fields.Selection(selection=[('new', 'New'),
                                        ('approved', 'Approved')],
                             default='new', tracking=True)
    student_id = fields.Many2one(
        'hostel.management.student.information',
        string='Student', ondelete='cascade', required=True)
    duration = fields.Integer(string='Duration', default=0,
                              compute='_compute_duration', store=True)

    @api.onchange('arrival_date', 'leave_date')
    def check_arrival(self):
        if self.arrival_date < self.leave_date:
            raise (ValidationError
                   ('Arrival date should greater than leave date.'))

    def button_approve(self):
        count = len(self.student_id.room_id.student_ids) - 1
        self.write({'state': 'approved'})
        if count == 0:
            cleaning = {
                'room_id': self.student_id.room_id.id,
                'start_time': self.leave_date,
                'state': 'new'
            }
            self.env['cleaning.service'].create(cleaning)

    @api.depends('arrival_date', 'leave_date')
    def _compute_duration(self):
        for rec in self:
            arrival_date = rec.arrival_date.date()
            leave_date = rec.leave_date.date()
            d1 = datetime.strptime(str(arrival_date), '%Y-%m-%d')
            d2 = datetime.strptime(str(leave_date), '%Y-%m-%d')
            duration = relativedelta(d1, d2).days
            rec.duration = duration
