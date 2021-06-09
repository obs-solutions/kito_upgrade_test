# -*- coding: utf-8 -*-

from odoo import fields, models, api


class PartnerRegion(models.Model):
    _name = "res.partner.region"
    _description = 'Partner Region'

    name = fields.Char(string='Region', required=True)


class PartnerBgGroup(models.Model):
    _name = "res.partner.bp"
    _description = 'BP Group'

    name = fields.Char(string='BP Group', required=True)


class Partner(models.Model):
    _inherit = "res.partner"

    ref = fields.Char(string='Customer Reference')
    fax = fields.Char('Fax')
    region_id = fields.Many2one('res.partner.region', string='Region')
    grade_id = fields.Many2one('res.partner.grade', 'Relationship', tracking=True)
    area_sales_manager = fields.Many2one('res.users', string='Area Sales Manager')
    is_competitor = fields.Boolean('Is Competitor')
    bp_group = fields.Many2one('res.partner.bp', 'BP Group')

    @api.model
    def create(self, vals):
        res = super(Partner, self).create(vals)
        if vals.get('area_sales_manager'):
            user_id = self.env['res.users'].sudo().browse(vals.get('area_sales_manager'))
            res.add_area_sm_followers(res.area_sales_manager, user_id)
        return res

    def write(self, vals):
        all_contacts = self  # + self.child_ids
        if vals.get('area_sales_manager'):
            user_id = self.env['res.users'].sudo().browse(vals.get('area_sales_manager'))
            for rec in self:
                rec.add_area_sm_followers(rec.area_sales_manager, user_id)
        return super(Partner, all_contacts).write(vals)

    def add_area_sm_followers(self, old_follower, new_follower):
        old_area_sales_manager = old_follower
        if old_area_sales_manager:
            old_follower = self.env['mail.followers'].search([('res_id', '=', self.id),
                                                              ('res_model', '=', 'res.partner'),
                                                              ('partner_id', '=', old_area_sales_manager.partner_id.id)])
            if old_follower:
                old_follower.sudo().unlink()
        partner_id = new_follower.partner_id
        follower_vals = {'res_id': self.id, 'res_model': 'res.partner', 'partner_id': partner_id.id}
        if partner_id:
            follower = self.env['mail.followers'].search([('res_id', '=', self.id),
                                                          ('res_model', '=', 'res.partner'),
                                                          ('partner_id', '=', partner_id.id)])
            if not follower:
                self.env['mail.followers'].create(follower_vals)
