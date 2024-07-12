# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):
    """Controller of student registration website form"""
    @http.route('/registration', type='http', auth="user", website=True)
    def register(self):
        """For getting Student Registration form"""
        rooms = (request.env['hostel.management.room.management'].
                 search([('state', 'in', ('empty', 'partial'))]))
        values = {
            'rooms': rooms
        }
        return request.render("hostel_management.Student-Registration",
                              values)

    @http.route('/hostel/room', type='json', auth="user", website=True)
    def room_details(self, **post):
        """Take rent of room  from database based on rpc call from js file"""
        rent = (request.env['hostel.management.room.management'].
                browse(int(post.get('room_number'))).total_rent)
        return rent

    @http.route('/registration/submit', type='http', auth='user',
                website=True, methods=['POST'])
    def registration_submit(self, **post):
        """Create new record in hostel.management.student.information table
        while clicking submit button in website student registration form"""
        room_id = int(post.get('room_id'))
        room = (request.env['hostel.management.room.management'].
                sudo().browse(room_id))
        if post.get('name') and post.get('email') and post.get('dob'):
            request.env['hostel.management.student.information'].create({
                'name': post.get('name'),
                'email': post.get('email'),
                'dob': post.get('dob'),
                'age': post.get('age'),
                'room_id': room_id
            })
        if not len(room.student_ids):
            room.write({'state': 'empty'})
        elif len(room.student_ids) < room.number_of_beds:
            room.write({'state': 'partial'})
        else:
            room.write({'state': 'full'})
        return request.render("hostel_management.register_success_popup")
