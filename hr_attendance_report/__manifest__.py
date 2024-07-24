{
    'name': "Day Wise Attendance Report",
    'version': '17.0.1.0',
    'application': True,
    'depends': ['base','contacts','hr',  'mail', 'web'],
    'author': 'SKR',
    'license': 'LGPL-3',
    'category': 'Human Resources/Attendances',
    'description': """
        Day Wise Attendance Report""",
    'installable': True,
    'data': [
        'report/day_wise_attendance_actions.report.xml',
        'report/day_wise_attendance_report.xml',
        'data/day_wise_attendance_report_mail.xml',
        'data/day_wise_attendance_report_recurring.xml'

    ]
}