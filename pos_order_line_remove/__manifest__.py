{
    'name': "POS Orderline Remove",
    'version': '17.0.1.0',
    'application': True,
    'depends': ['base','point_of_sale', 'web', 'website', 'website_sale'],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Point of Sale',
    'description': """
     POS Orderline Remove module""",
    'installable': True,
    'data': [
    ],
   'assets':{
       'point_of_sale._assets_pos':[
        'pos_order_line_remove/static/src/xml/orderline_remove.xml',
        'pos_order_line_remove/static/src/xml/orderlines_all_clear.xml',
        'pos_order_line_remove/static/src/js/orderline_remove.js',
        'pos_order_line_remove/static/src/js/custombutton_clear_lines.js',
        'pos_order_line_remove/static/src/js/pay.js'

       ],
   },

    }