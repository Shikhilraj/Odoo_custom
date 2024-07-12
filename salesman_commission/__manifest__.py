{
    'name' : "Salesman Commision",
    'version': '17.0.1.0',
    'application':True,
    'depends': ['account', 'base', 'contacts', 'mail', 'sale', 'stock', 'web'],
    'description': """ Salesman Commision""",
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Sales',
    'installable': True,
    'data':[
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/salesman_commission_view.xml',
        'views/salesman_commission_menu.xml'

    ]
}