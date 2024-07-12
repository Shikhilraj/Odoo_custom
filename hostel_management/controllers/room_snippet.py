# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class RoomSnippet(http.Controller):

    @http.route(['/new_rooms'], type='json', auth="user", website=True)
    def all_rooms(self):
        """Get the Latest rooms from Hostel management """
        rooms = (request.env['hostel.management.room.management'].
                 search_read([], ['room_number', 'room_type', 'total_rent',
                                  'id', 'image'],
                             order='create_date desc'))

        return rooms

    @http.route(['/room/<int:id>'], type='http', auth='user', website=True)
    def get_room(self, **post):
        """Get single room from database. """
        room = (request.env['hostel.management.room.management'].
                browse(post.get('id')))
        return request.render('hostel_management.single_room_snippet',
                              {'room': room})

