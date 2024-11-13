{
    'name': 'RADIUS Management',
    'version': '1.0',
    'summary': 'Manage RADIUS attributes and accounting records',
    'category': 'Tools',
    'author': 'Bigmachini Enterprises LTD',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hotspot_user_views.xml',
        'views/res_partner.xml',
        'views/hotspot_profile.xml',
        'views/hotspot_profile_limitations.xml',
    ],
    'installable': True,
    'application': True,
}
