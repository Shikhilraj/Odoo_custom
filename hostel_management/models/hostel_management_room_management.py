# -*- coding: utf-8 -*-
from odoo import api, fields, models


class RoomManagement(models.Model):
    _name = "hostel.management.room.management"
    _description = "Room Management"
    _inherit = ['mail.thread']
    _rec_name = 'room_number'

    room_number = fields.Char(string="Room Number", readonly=True,
                              default='New', tracking=True, copy=False)
    room_type = fields.Selection(
        selection=[('double', 'Double'),
                   ('single', 'Single'),
                   ('quad', 'Quad'),
                   ('triple', 'Triple')], string="Room Type")
    number_of_beds = fields.Integer(string="Number of Beds", default=1)
    rent = fields.Float(string="Rent")

    state = fields.Selection(
        selection=[('empty', 'Empty'),
                   ('partial', 'Partial'),
                   ('full', 'Full'),
                   ('cleaning', 'Cleaning')],
        string="State", tracking=True, default='empty', clickable="1")
    company_id = fields.Many2one('res.company', readonly=True,
                                 string='Company',
                                 default=lambda self:
                                 self.env.user.company_id.id)
    currency_id = fields.Many2one(related='company_id.currency_id',
                                  string='Currency', readonly=True)
    student_ids = fields.One2many(
        'hostel.management.student.information',
        inverse_name='room_id', string="Student", readonly=True)
    facilities_ids = fields.Many2many(
        'hostel.management.facilities', string='Facilities',
        relation="rel_facilities_room")
    total_rent = fields.Float(string='Total Rent', default=0,
                              compute='compute_total', store=True)
    pending_amount = fields.Monetary(string='Pending Amount', default=0,
                                     compute='_compute_pending_amount',
                                     store=True)
    image = fields.Image(string='Image', store=True)

    @api.model
    def create(self, value):
        """Generate Sequence number"""
        value['room_number'] = (self.env['ir.sequence'].
                                next_by_code('room.number'))
        return super(RoomManagement, self).create(value)

    @api.depends('rent', 'facilities_ids')
    def compute_total(self):
        """Calculate the total rent"""
        for rec in self:
            total_rent = rec.rent
            for facility in rec.facilities_ids:
                total_rent = total_rent + facility.charge
            rec.total_rent = total_rent

    def button_invoice(self):
        """Create invoice"""
        for std_info in self.student_ids:
            monthly_invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'invoice_date': fields.Date.today(),
                'partner_id': std_info.partner_id.id,
                'student_id': std_info.id,
                'amount_total': self.total_rent,
                'invoice_line_ids': [
                    (0, None, {
                        'product_id': 66,
                        'quantity': 1,
                        'price_unit': self.total_rent,
                        'price_subtotal': self.total_rent,
                        'tax_ids': []
                    }), ],
            })
            self._compute_pending_amount()
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'tree,form',
                'view_mode': 'tree,form',
                'res_id': monthly_invoice.id,
                'res_model': 'account.move',
                'context': "{'type':'out_invoice',"
                           "'create':'True',"
                           "'state':'draft'}",
                'domain': [('student_id.room_id', '=', self.room_number),
                           ('state', '=', 'draft')]
            }

    @api.depends('student_ids.payment_status')
    def _compute_pending_amount(self):
        pending_amount = 0
        for record in self.student_ids:
            pending_invoices = (record.env['account.move'].
                                search([('student_id', '=', record.id)]))
            for rec in pending_invoices:
                if rec.payment_state == 'not_paid':
                    pending_amount = pending_amount + rec.amount_total
        self.pending_amount = pending_amount
