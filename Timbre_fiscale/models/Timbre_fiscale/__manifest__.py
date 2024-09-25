# -*- coding: utf-8 -*-
{
    'name': "Facturation",
    'version': '1.0',
    'summary': 'Factures & Paiements',
    'description': "",
    'sequence': -100,
    'category': 'comptabilité',
    'depends':["base","account","sale"],
    'data':['views/account_tax.xml',
            'views/res_partner.xml',
            'views/account_move.xml',
            'report/rapport.xml',
            'report/template_declaration.xml',
            'report/inherit_facture.xml',
            'report/template_facture.xml',
            'views/menu.xml',
            'report/header.xml',
            'data/ir_cron.xml'

            ],

    'installable': True,
    'auto_install': True,
    'application': True,
    'license': 'LGPL-3',
}
