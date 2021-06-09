# -*- coding: utf-8 -*-

from odoo import models


class Followers(models.Model):
    _inherit = 'mail.followers'

    def _insert_followers(self, res_model, res_ids, partner_ids, partner_subtypes, channel_ids, channel_subtypes,
                          customer_ids=None, check_existing=False, existing_policy='skip'):

        sudo_self = self.sudo().with_context(default_partner_id=False, default_channel_id=False)
        partner_ids = self.env['res.partner'].browse(partner_ids).filtered(lambda x: not x.partner_share).ids
        if not partner_subtypes and not channel_subtypes:  # no subtypes -> default computation, no force, skip existing
            new, upd = self._add_default_followers(res_model, res_ids, partner_ids, channel_ids, customer_ids=customer_ids)
        else:
            new, upd = self._add_followers(res_model, res_ids, partner_ids, partner_subtypes, channel_ids, channel_subtypes, check_existing=check_existing, existing_policy=existing_policy)
        if new:
            sudo_self.create([
                dict(values, res_id=res_id)
                for res_id, values_list in new.items()
                for values in values_list
            ])
        for fol_id, values in upd.items():
            sudo_self.browse(fol_id).write(values)
