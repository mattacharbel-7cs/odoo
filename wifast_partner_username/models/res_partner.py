# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Declare the custom field. Odoo will map this to the existing DB column 'x_username'.
    x_username = fields.Char(string='Username', help='Custom username for contacts')
