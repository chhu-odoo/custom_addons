{
    'name': 'Motorcycle Registry',
    'summary': 'Manage Registration of Motorcycles',
    'description': """Motorcycle Registry
        ====================
        This Module is used to keep track of the Motorcycle Registration and Ownership of each motorcycled of the brand.""",
    'author': 'chhu-odoo',
    'website': 'https://github.com/chhu-odoo/custom_addons',
    'category': 'Kawiil/Motorcycle Registry',
    'depends': ['stock', 'website'],
    'license': 'OEEL-1',
    'data': [
        'security/registry_groups.xml',
        'security/ir.model.access.csv',
        'data/registry_number_data.xml',
        'views/registry_menuitems.xml',
        'views/registry_views.xml',
        'views/product_template_inherit.xml',
        'views/motorcycle_registry_templates.xml'
    ],
    'demo': [
        'demo/registry_demo.xml',
        'demo/product_demo.xml'
    ],
    'application': True
}