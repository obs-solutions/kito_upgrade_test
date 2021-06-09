# -*- coding: utf-8 -*-
{
    'name': 'KITO Helpdesk&CRM',
    'version': '1.0',
    'category': 'General',
    'description': """
        KITO customization (AVP)
    """,
    'author': 'OBS',
    'depends': [
        'crm',
        'project',
        'helpdesk',
        'website_helpdesk',
        'crm_helpdesk',
        'website_crm_partner_assign'
    ],
    'data': [
            'data/res.lang.csv',
            'data/ir_sequence_data.xml',
            'views/partner_view.xml',
            'views/crm_view.xml',
            'views/helpdesk_view.xml',
            'views/mail_data.xml',
            'security/ir.model.access.csv',
            'wizard/helpdesk_ticket_merge_view.xml',
            'views/res_bank_view.xml',
            'views/res_company_view.xml'
    ],
    'qweb': [

    ],
    'installable': True,
    'auto_install': False,
}
