{
    'name': 'QWeb Tutorial',
    'version': '17.0.1.0.0',
    'category': 'Tools',
    'summary': 'Module to teach QWeb rendering',
    'depends': ['base', 'mail', 'web'],
    'data': [

        'security/ir.model.access.csv',

        'data/qweb_tutorial_data.xml',
        'views/qweb_tutorial_views.xml',
        'views/templates.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
