# -*- coding: utf-8 -*-
{
    'name': 'Lot & Serail Number',
    'version': '17.0.1.0',
    'application':True,
    'depends': ['account', 'base', 'contacts', 'mail', 'sale', 'stock', 'web'],
    'description': """ Salesman Commision""",
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Inventory',
    'installable': True,
    'data':[
        'security/ir.model.access.csv',
        'wizards/import_lot_serial_wizard_view.xml',
        'wizards/success_wizard_view.xml'
    ]
}