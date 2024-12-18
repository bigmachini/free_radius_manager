{
    'name': 'RADIUS Management',
    'version': '1.0',
    'summary': 'Manage RADIUS attributes and accounting records',
    'category': 'Tools',
    'author': 'Bigmachini Enterprises LTD',
    'depends': ['base','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'security/radius_manager_security.xml',
        'views/assign_user_profile_wizard.xml',
        'views/hotspot_user_views.xml',
        'views/res_partner.xml',
        'views/hotspot_profile.xml',
        'views/hotspot_limitations.xml',
        'views/hotspot_user_sessions.xml',
        'views/hotspot_profile_limitation.xml',
        'views/user_profile_limitation.xml',
        'views/hotspot_router.xml',
        'data/cron_jobs.xml',
    ],
    'installable': True,
    'application': True,
}
