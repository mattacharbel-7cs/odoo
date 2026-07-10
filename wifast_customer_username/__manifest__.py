{
    'name': 'WiFast Customer Username',
    'version': '19.0.1.0.2',
    'summary': 'Adds a WiFi/customer account username to contacts with a secured API.',
    'author': 'Dow Group',
    'website': 'https://www.dowgroup.com',
    'category': 'Contacts',
    'license': 'LGPL-3',
    'depends': ['contacts'],
    'data': [
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
