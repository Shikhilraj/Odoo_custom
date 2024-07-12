{
    'name': "Hostel Management",
    'version': '17.0.1.0',
    'application': True,
    'depends': ['base', 'mail',  'web', 'account', 'base_automation', 'contacts',
                 'website'],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Others',
    'description': """
    Hostel Management module """,
    'installable': True,
    'data': [
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'data/room_number_sequence.xml',
        'data/student_id_sequence.xml',
        'data/rent_product_data.xml',
        'data/hostel_management_facilities_data.xml',
        'data/user_data.xml',
        'data/hostel_rent_email_template.xml',
        'data/monthly_invoice_recurring.xml',
        'views/room_management_view.xml',
        'views/hostel_invoice_view.xml',
        'views/hostel_management_facilities.xml',
        'views/student_information_view.xml',
        'views/leave_request_view.xml',
        'views/cleaning_service_view.xml',
        'views/website_student_registration_form.xml',
        'views/register_success_popup.xml',
        'views/room_snippet_template.xml',
        'views/static_snippet.xml',
        'wizards/student_report_filter_wizard_view.xml',
        'wizards/leave_request_report_wizard_view.xml',
        'reports/student_report_template.xml',
        'reports/student_report_action.xml',
        'reports/leave_request_report_template.xml',
        'reports/leave_request_report_action.xml',
        'views/hostel_management_menu.xml',
        'views/student_registration_web_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
                    'hostel_management/static/src/js/action_manager.js',
                ],
        'web.assets_frontend': [
                    'hostel_management/static/src/css/student_registration.css',
                    'hostel_management/static/src/js/student_registration.js',
                    'hostel_management/static/src/xml/dynamic_courosel.xml',
                    'hostel_management/static/src/js/room_dynamic_snippet.js',
        ]
    }

}
