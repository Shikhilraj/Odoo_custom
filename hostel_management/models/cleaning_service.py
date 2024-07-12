# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import ValidationError


class CleaningService(models.Model):
    _name = 'cleaning.service'
    _description = 'Cleaning Service'
    _inherit = ['mail.thread']
    _rec_name = 'room_id'
    room_id = fields.Many2one('hostel.management.room.management',
                              string='Room')
    start_time = fields.Datetime(string='Start Time')
    user_id = fields.Many2one('res.users', string='Cleaning Staff',
                              default=lambda self: self.env.user.id)
    state = fields.Selection(selection=[('new', 'New'),
                                        ('assigned', 'Assigned'),
                                        ('done', 'Done')], default='new',
                             tracking=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id)

    def button_assign(self):
        self.write({'state': 'assigned'})
        self.room_id.write({'state': 'cleaning'})

    def button_complete(self):
        if self.state == 'assigned':
            self.write({'state': 'done'})
            if len(self.room_id.student_ids) == 0:
                self.room_id.write({'state': 'empty'})
            elif self.room_id.number_of_beds == len(self.room_id.student_ids):
                self.room_id.write({'state': 'full'})
            else:
                self.room_id.write({'state': 'partial'})
        else:
            raise ValidationError('Cleaning service should be assign to '
                                  'staff before completing the state.')
