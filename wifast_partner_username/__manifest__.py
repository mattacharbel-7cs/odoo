# -*- coding: utf-8 -*-
{
    'name': 'WiFast Partner Username',
    'version': '1.0',
    'summary': 'Add Username field next to Contact Name',
    'description': """
        Adds a custom username field (x_username) next to the partner name title in contact form views.
    """,
    'author': 'WiFast DevOps',
    'website': 'https://www.wifast.net',
    'category': 'Contacts',
    'depends': ['base', 'contacts'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
