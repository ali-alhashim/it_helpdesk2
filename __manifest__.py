# __manifest__.py

{
    'name': 'IT Helpdesk 2',
    'version': '1.0',
    'category': 'IT',
    'description': 'IT Helpdesk management system',
    'author': 'Ali Musa  Alhashim',
    'website': 'https://www.ali-alhashim.com',
    'license': 'AGPL-3',
    'depends': ['base', 'hr','mail'],
    'data': [
        'data/security.xml',
        'security/ir.model.access.csv',
        
        'views/cancel_confirm_wizard_views.xml',
        'views/solution_input_wizard_views.xml',
        'data/assets_sequence.xml',
        'views/it_request_view.xml',
        "report/report_it_asset_document.xml",
        'views/report_it_asset_action.xml',
        'views/it_ticket_view.xml',
        'views/it_support_assign_wizard_view.xml',
        'views/it_device_view.xml',
        'views/hr_employee_view.xml',
        'views/it_device_user_history_view.xml',
        'views/menu.xml',
        'security/it_helpdesk_security.xml',
    ],
    
    'static': [
        'static/src/img/logo.png',
    ],

    'demo': [],
    'installable': True,
    'application': True,
}