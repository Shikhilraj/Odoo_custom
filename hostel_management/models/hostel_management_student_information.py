# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class StudentInformation(models.Model):
    _name = "hostel.management.student.information"
    _description = "Hostel Management Student Information"
    _inherit = 'mail.thread'
    _sql_constraints = [('email_unique', 'unique(email)',
                         'Email is already used')]

    name = fields.Char(required=True, String='Name', copy=False)
    student_number = fields.Char(readonly=True, string='Student Number')
    address = fields.Text(string='Address')
    dob = fields.Date(required=True, string='DOB', default=datetime.today())
    room_id = fields.Many2one('hostel.management.room.management',
                              string='Room', readonly=True)
    email = fields.Char(string='Email', required=True)
    image = fields.Image(string='Image')
    receive_mail = fields.Boolean(string='Receive mail', default=False)
    street = fields.Char(string='Street1')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    zip = fields.Char(string='Zip')
    state_id = fields.Many2one(comodel_name='res.country.state', string='State',
                               domain="[('country_id', '=', country_id)]")
    country_id = fields.Many2one(string="Country", comodel_name='res.country')
    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 default=lambda self:
                                 self.env.user.company_id.id)
    age = fields.Char(string='Age', compute='compute_age', store=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 compute='_compute_search_partner')
    active = fields.Boolean('Active', default=True)
    invoice_count = fields.Integer(compute='_compute_count')
    currency_id = fields.Many2one(related='company_id.currency_id',
                                  string='Currency', readonly=True)
    monthly_amount = fields.Monetary(string='Monthly Amount', readonly=True,
                                     default=0,
                                     compute='_compute_monthly_amount')
    invoice_status = fields.Selection(
        selection=[('pending', 'Pending'),
                   ('done', 'Done')], string='Invoice status', store=True)

    payment_status = fields.Selection(
        selection=[('draft', 'Draft'),
                   ('pending', 'Pending'),
                   ('done', 'Done')],
        default='draft', compute='_compute_payment_status', store=True)
    user_id = fields.Many2one('res.users', string='User',
                              compute='_compute_student_user_search',
                              store=True)
    pending_amount = fields.Float(string='Pending Amount', default=0,
                                  compute='_compute_pending_amount', store=True)

    @api.model
    def create(self, value):
        """Sequence generating for student number"""
        value['student_number'] = (self.env['ir.sequence'].
                                   next_by_code('stud.id'))
        return super(StudentInformation, self).create(value)

    def button_allocate(self):
        """Room Allocation """

        if self.room_id.room_number is False:   # check the room_id is empty
            room_id = self.env['hostel.management.room.management'].search(
                domain=[('state', 'not in', ['full', 'cleaning'])], limit=1)
            if len(room_id.ids) > 0:
                self.write({'room_id':
                            self.env['hostel.management.room.management'].
                            search(domain=[('state', 'not in',
                                           ['full', 'cleaning'])], limit=1)})
                if len(self.room_id.student_ids) < self.room_id.number_of_beds:
                    self.room_id.write({
                        'state': 'partial'
                    })
                elif (len(self.room_id.student_ids) ==
                      self.room_id.number_of_beds):
                    self.room_id.write({
                        'state': 'full'
                    })
            else:
                raise ValidationError('Room not available')
        else:
            raise ValidationError('Already Allocated')

    @api.depends('dob')
    def compute_age(self):
        """Age Calculation from date of birth"""
        for rec in self:
            if rec.dob:
                d1 = datetime.strptime(str(rec.dob), "%Y-%m-%d").date()
                d2 = date.today()
                age = relativedelta(d2, d1).years
                if age < 0:
                    raise ValidationError("Choose valid DOB")
                rec.age = age

    @api.depends('room_id')
    def _compute_monthly_amount(self):
        """Compute """
        self.write({'monthly_amount': self.room_id.total_rent})

    @api.depends('pending_amount')
    def _compute_payment_status(self):
        """ Payment status based on payment state in invoices."""
        for rec in self:
            user_invoice = (rec.env['account.move'].
                            search([('student_id', '=', rec.id)]))
            if rec.id == user_invoice.student_id.id:
                for record in user_invoice:
                    payment_state = record.payment_state
                    if payment_state == 'not_paid':
                        rec.write({'payment_status': 'pending'})
                        break
                    elif payment_state == 'paid':
                        rec.write({'payment_status': 'done'})
            else:
                rec.payment_status = 'draft'

    def _compute_count(self):
        """Invoice count"""
        for rec in self:
            rec.invoice_count = (rec.env['account.move'].search_count(
                [('student_id', '=', rec.id)]))

    def get_invoices(self):
        """For getting student invoice."""
        self._compute_pending_amount()
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_type': 'tree,form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'res_id': self.id,
            'context': {'type': 'out_invoice', 'create': 'True'},
            'domain': [('student_id', '=', self.id)]
        }

    def button_vacate(self):
        """Remove the room from student model. And also archive the student
        when clicking these button."""
        room_id = self.room_id
        self.write({'active': False})
        count = len(room_id.student_ids)
        if count == 0:
            room_id.write({'state': 'cleaning'})
            cleaning_service = {'room_id': room_id.id,
                                'state': 'new'}
            self.env['cleaning.service'].create(cleaning_service)
        elif count < room_id.number_of_beds:
            room_id.write({'state': 'partial'})
        return self.ids

    def monthly_rent_invoice(self):
        """Create the invoices automatically on the first day of each
        month and send an email to the student"""

        student_information = (
            self.env['hostel.management.student.information'].
            search([('active', '=', True)]))
        for record in student_information:
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.partner_id.id,
                'invoice_date': fields.Date.context_today(record),
                'student_id': record.id,
                'amount_total': record.room_id.total_rent,
                'invoice_line_ids': [
                    (0, 0, {
                        'product_id': 66,
                        'quantity': 1,
                        'price_unit': record.room_id.total_rent,
                        'price_subtotal': record.room_id.total_rent
                    }), ],
            })
            invoice.action_post()

    def user_create(self):
        """Create user when student is created"""
        values = self.search([], order='id desc', limit=1)
        for rec in values:
            self.env['res.users'].create({
                'name': rec.name,
                'login': rec.email
            })

    @api.depends('student_number')
    def _compute_student_user_search(self):
        """Fill the user field automatically when student is created"""
        for rec in self:
            user = rec.env['res.users'].search([('login', '=', rec.email)])
            rec.user_id = user

    @api.depends('user_id')
    def _compute_search_partner(self):
        """Search the partner"""
        for rec in self:
            rec.partner_id = rec.user_id.partner_id

    @api.depends('invoice_count', 'room_id.pending_amount')
    def _compute_pending_amount(self):
        for rec in self:
            user_invoice = (rec.env['account.move'].search([]).
                            filtered(lambda x: x.student_id.id == rec.id))
            pending_amount = 0
            for state in user_invoice:
                if state.payment_state == 'not_paid':
                    pending_amount = pending_amount + state.amount_total
                self.pending_amount = pending_amount


