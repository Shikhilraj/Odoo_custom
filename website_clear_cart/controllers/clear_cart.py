# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class WebsiteSaleClearCart(http.Controller):

    @http.route('/website_sale/clear_cart', type='json', auth="user",
                website=True)
    def clear_cart(self, **post):
        """unlink the carted from products from 'sale.order' model"""
        (request.env['sale.order'].browse(request.website.sale_get_order().id).
         order_line.unlink())
        return
