# -*- coding: utf-8 -*-
{
    'name': 'WiFast Partner Username',
    'version': '19.0.1.1.0',
    'summary': 'Username field next to Contact Name + secured external API.',
    'description': """
        Adds the custom @username field (x_studio_username) next to the partner
        name in the contact form, and exposes a secured HTTP API to read and
        update the username from external systems (WiFast / Fast2Serv).
    """,
    'author': 'WiFast DevOps / Dow Group',
    'website': 'https://www.wifast.net',
    'category': 'Contacts',
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'wifast_partner_username/static/src/css/username.css',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
