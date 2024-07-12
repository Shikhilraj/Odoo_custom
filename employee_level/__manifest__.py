{
    'name': "Employeee Level",
    'version': '17.0.1.0',
    'application': True,
    'depends': ['base','contacts','hr',  'mail', 'web'],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Others',
    'description': """
        Employeee Level module""",
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/employee_level_view.xml',
        'views/hr_employee_view.xml',
        'views/employee_level_menu.xml',
    ]
}