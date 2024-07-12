{
    'name': "Payment Provider : PayU",
    'version': '17.0.1.0',
    'depends': ['payment' ],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Accounting/Payment Providers',
    'description': """
     Payment Provider : PayU""",
    'application': True,
    'data': [

        'data/payment_method_payu.xml',
        'views/payment_payu_template.xml',
        'views/payment_provider_view.xml',

        'data/payment_provider_data.xml',

    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',

   }