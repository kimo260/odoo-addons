# -*- coding: utf-8 -*-
{
    'name': 'Stock Traceability Report',
    'version': '1.0',
    'category': 'Warehouse Management',
    'sequence': 14,
    'summary': '',
    'description': """
Stock Traceability Report
=========================

    """,
    'author':  'ADHOC',
    'website': 'www.adhoc.com.ar',
    'images': [
    ],
    'depends': [
        'stock',
        'report_aeroo',
    ],
    'data': ['report/stock_lot_report.xml'
             ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
