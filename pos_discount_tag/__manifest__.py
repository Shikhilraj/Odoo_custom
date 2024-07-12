{
    'name': "POS Discount Tag",
    'version': '17.0.1.0',
    'application': True,
    'depends': ['base','point_of_sale', 'web', 'website', 'website_sale'],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Point of Sale',
    'description': """
     POS Discount Tag module""",
    'installable': True,
    'data': [
        'views/product_product_view.xml',

    ],
   'assets':{
       'point_of_sale._assets_pos':[
           'pos_discount_tag/static/src/xml/product_list_widget_inherit.xml',
           'pos_discount_tag/static/src/js/custom_pos_receipt.js',
           'pos_discount_tag/static/src/css/pos_card.css',
           'pos_discount_tag/static/src/xml/pos_card.xml',
           'pos_discount_tag/static/src/xml/custom_pos_receipt.xml',

       ],
   },

    }