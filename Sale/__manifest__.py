{
    'name': " Credit Limit",
    'version': '17.0.1.0',
    'application':True,
    'depends': ['account', 'base', 'contacts', 'mail', 'sale', 'stock', 'web'],
    'description': """ Sale Order Credit Limit""",
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Sales',
    'installable': True,
    'data': [
        'views/respartner_credit_limit_view.xml',
        'views/sale_order_view.xml'
 ]
}