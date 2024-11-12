{
    'name': 'FreeRADIUS Management',
    'version': '1.0',
    'summary': 'Manage FreeRADIUS attributes and accounting records',
    'category': 'Tools',
    'author': 'Bigmachini Enterprises LTD',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/radcheck_views.xml',
        'views/radreply_views.xml',
        'views/radacct_views.xml',
        'views/radusergroup_views.xml',
        'views/radgroup_views.xml',
    ],
    'installable': True,
    'application': True,
}
