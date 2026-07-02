# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Declare the existing studio username field to map directly to the database column
    x_studio_username = fields.Char(string='UserName', help='Custom username for contacts (Studio)')

    @api.depends('x_studio_username')
    def _compute_display_name(self):
        # Call the default display name computation first
        super()._compute_display_name()
        for partner in self:
            # If the contact has a username, append it to the display name in parentheses
            if partner.x_studio_username and partner.display_name:
                partner.display_name = f"{partner.display_name} (@{partner.x_studio_username})"
