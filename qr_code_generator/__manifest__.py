{
    'name': "QR Code Generator",
    'version': '17.0.1.0',
    'application': True,
    'depends': ['base', 'web', 'website'],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Others',
    'description': """
        QR Code Generator""",
    'installable': True,
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'qr_code_generator/static/src/js/systray_icon.js',
            'qr_code_generator/static/src/xml/systray_icon.xml',

        ]
    }

}