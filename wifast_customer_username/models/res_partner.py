# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    wifi_username = fields.Char(
        string='Username',
        copy=False,
        index=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if isinstance(vals.get('wifi_username'), str):
                vals['wifi_username'] = vals['wifi_username'].strip()
        return super().create(vals_list)

    def write(self, vals):
        if isinstance(vals.get('wifi_username'), str):
            vals = dict(vals, wifi_username=vals['wifi_username'].strip())
        return super().write(vals)

    @api.constrains('wifi_username', 'company_id')
    def _check_wifi_username_unique_per_company(self):
        for partner in self:
            username = (partner.wifi_username or '').strip()
            if not username:
                continue

            duplicate = self.with_context(active_test=False).search([
                ('id', '!=', partner.id),
                ('wifi_username', '=', username),
                ('company_id', '=', partner.company_id.id or False),
            ], limit=1)
            if duplicate:
                raise ValidationError(_(
                    "The WiFi username must be unique within the same company."
                ))
