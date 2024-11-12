{
    'name': 'FreeRADIUS Management',
    'version': '1.0',
    'summary': 'Manage FreeRADIUS attributes and accounting records',
    'category': 'Tools',
    'author': 'Bigmachini Enterprises LTD',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/radcheck_views.xml',
    ],
    'installable': True,
    'application': True,
}
