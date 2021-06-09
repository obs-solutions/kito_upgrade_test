# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'syscoon Finanzinterface - DATEV ASCII Export',
    'version': '14.0.0.0.12',
    'author': 'syscoon GmbH',
    'license': 'OPL-1',
    'website': 'https://syscoon.com',
    'summary': 'DATEV ASCII Export ',
    'description': """The module account_financeinterface_datev provides the DATEV ASCII Export.""",
    'category': 'Accounting',
    'depends': [
        'syscoon_financeinterface',
        'syscoon_partner_accounts',
    ],
    'data': [
        'views/account_move_views.xml',
        'views/account_views.xml',
        'views/res_config_settings.xml',
        'views/syscoon_financeinterface.xml',
        'wizards/syscoon_financeinterface_export.xml',
    ],
    'active': False,
    'installable': True,
}
