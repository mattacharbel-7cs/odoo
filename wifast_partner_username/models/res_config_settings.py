# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wifast_customer_username_api_key = fields.Char(
        string='WiFi API Key',
        config_parameter='wifast_customer_username.api_key',
    )
