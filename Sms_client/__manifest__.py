# -*- coding: utf-8 -*-
{
    'name': "SMS",
    'version': '1.0',
    'summary': 'Send sms',
    'description': "",
    'sequence': -100,
    'category': '',
    'depends':["base","account"],
    'data' : ['views/sms.xml',
              ],


    'installable': True,
    'auto_install': True,
    'application': True,
    'license': 'LGPL-3',
}
