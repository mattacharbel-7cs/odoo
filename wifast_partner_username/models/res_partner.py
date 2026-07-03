# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Declare the existing studio username field to map directly to the database column
    x_studio_username = fields.Char(string='UserName', help='Custom username for contacts (Studio)')

    @api.depends('x_studio_username', 'parent_id.x_studio_username')
    def _compute_display_name(self):
        super()._compute_display_name()
        for partner in self:
            # Fallback: Inherit parent username for display name if still empty
            username = partner.x_studio_username
            if not username and partner.parent_id:
                username = partner.parent_id.x_studio_username

            if username and partner.display_name:
                suffix = f" (@{username})"
                if not partner.display_name.endswith(suffix):
                    partner.display_name = f"{partner.display_name}{suffix}"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Automatically copy parent's username to subcontacts on creation
            if 'parent_id' in vals and not vals.get('x_studio_username'):
                parent = self.env['res.partner'].browse(vals['parent_id'])
                if parent.exists() and parent.x_studio_username:
                    vals['x_studio_username'] = parent.x_studio_username
        return super(ResPartner, self).create(vals_list)

    def write(self, vals):
        # Automatically copy parent's username to subcontacts when modified
        res = super(ResPartner, self).write(vals)
        if 'parent_id' in vals or 'x_studio_username' in vals:
            for partner in self:
                if partner.parent_id and not partner.x_studio_username:
                    if partner.parent_id.x_studio_username:
                        # Write directly to database to avoid infinite recursion
                        partner.write({'x_studio_username': partner.parent_id.x_studio_username})
        return res
