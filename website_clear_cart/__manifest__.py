{
    'name': "Clear Cart",
    'version': '17.0.1.0',
    'application': True,
    'depends': ['base', 'web', 'website', 'website_sale'],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Website',
    'description': """
     Website Clear Cart module""",
    'installable': True,
    'data': [
        'views/clear_cart_view.xml'

    ],
    'assets': {
        'web.assets_frontend': [
            'website_clear_cart/static/src/js/clear_cart.js',
        ]
    }

}