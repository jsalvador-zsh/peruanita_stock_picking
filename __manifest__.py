# -*- coding: utf-8 -*-
{
    'name': 'Peruanita Stock Picking Control',
    'version': '18.0.1.0.0',
    'summary': 'Control de despacho para entregas de stock picking',
    'description': """
        Este módulo agrega una nueva pestaña de control de despacho
        para los registros de entrega en stock.picking.
        
        Características:
        - Nueva pestaña visible solo para picking_type_code = 'outgoing'
        - Campos para datos generales de transporte
        - Control de documentación enviada del producto
    """,
    'author': 'Juan Salvador',
    'website': 'https://jsalvador.dev',
    'category': 'Inventory/Inventory',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/stock_temperature_control_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}