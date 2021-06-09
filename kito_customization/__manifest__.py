{
    #  Information
    'name': 'Kito Customization',
    'version': '14.0.1',
    'summary': 'Kito Customization',
    'description': 'Kito Customization',
    'category': 'custom',

    # Author
    'author': 'Odoo-Ps',
    'website': 'https://www.odoo.com',
    'license': '',

    # Dependency
    'depends': ['sale_management', 'purchase', 'stock', 'repair', 'website_crm_partner_assign'],
    'data': [
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
        'views/purchase_oder_views.xml',
        'views/res_partner_grade.xml',
        'reports/barcode_report_templates.xml'
    ],

    # Other
    'installable': True,
    'auto_install': False,
}
