{
    'name': "Customer Sale",
    'version': '17.0.1.0',
    'application': True,
    'depends': ['base','contacts', 'mail', 'sale', 'stock'],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Others',
    'description': """
        Customer Sale module""",
    'installable': True,
    'data': [
        'views/res_partner_view.xml',
        'views/product_template_view.xml'

    ]
}