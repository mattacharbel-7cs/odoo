# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Declare the existing studio username field to map directly to the database column
    x_studio_username = fields.Char(string='UserName', help='Custom username for contacts (Studio)')

    @api.depends('x_studio_username', 'parent_id.x_studio_username')
    def _compute_display_name(self):
        # Call the default display name computation first
        super()._compute_display_name()
        for partner in self:
            # Inherit parent username if this partner does not have one explicitly set
            username = partner.x_studio_username
            if not username and partner.parent_id:
                username = partner.parent_id.x_studio_username

            if username and partner.display_name:
                suffix = f" (@{username})"
                # Prevent duplicate appends
                if not partner.display_name.endswith(suffix):
                    partner.display_name = f"{partner.display_name}{suffix}"
