# -*- coding: utf-8 -*-

from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"

    referred = fields.Char(string='Customer Reference')
    sap_ref = fields.Char('SAP Reference')
    is_competitor = fields.Boolean('Is Competitor')
    industry_id = fields.Many2one('res.partner.industry', string='Industry')
    grade_id = fields.Many2one('res.partner.grade', string='Relationship')
    region_id = fields.Many2one('res.partner.region', string='Region')
    bp_group = fields.Many2one('res.partner.bp', 'BP Group')
    area_sales_manager = fields.Many2one('res.users', string='Area Sales Manager')
    number = fields.Char(string="Opportunity ID")

    @api.model
    def create(self, values):
        res = super(CrmLead, self).create(values)
        res.number = self.env['ir.sequence'].next_by_code('crm.lead.seq')
        parent_dict = self.env['mail.thread']._message_get_default_recipients_on_records(res)
        if res.partner_id:
            res.message_subscribe([res.partner_id.id])
        if res.area_sales_manager:
            res.message_subscribe([res.area_sales_manager.partner_id.id])

        email_cc = parent_dict[res.id]['email_cc']
        if email_cc:
            cc_mails = email_cc.split(',')
            for cc in cc_mails:
                partner = self.env['res.partner'].search([('email', '=', cc)])
                if partner:
                    res.message_subscribe([partner.id])

        if values.get('area_sales_manager', False):
            user_id = self.env['res.users'].sudo().browse(values.get('area_sales_manager'))
            res.add_area_sm_followers(res.area_sales_manager, user_id, False)
        elif not values.get('area_sales_manager', False) and res.partner_id:
            user_id = res.partner_id.area_sales_manager
            res.add_area_sm_followers(res.partner_id.area_sales_manager, user_id, False)
        return res

    def write(self, vals):
        if vals.get('type') == 'opportunity':
            for rec in self:
                if rec.partner_id:
                    partner = rec.partner_id
                    lang = partner.lang or partner.parent_id.lang
                    if lang:
                        lang = self.env['res.lang'].search([('code', '=', lang)])
                    rec.phone = partner.phone or partner.parent_id.phone
                    rec.industry_id = partner.industry_id.id or partner.parent_id.industry_id.id
                    rec.grade_id = partner.grade_id.id or partner.parent_id.grade_id.id
                    rec.region_id = partner.region_id.id or partner.parent_id.region_id.id
                    rec.bp_group = partner.bp_group.id or partner.parent_id.bp_group.id
                    rec.is_competitor = partner.is_competitor or partner.parent_id.is_competitor
                    rec.street = partner.street or partner.parent_id.street
                    rec.street2 = partner.street2 or partner.parent_id.street2
                    rec.city = partner.city or partner.parent_id.city
                    rec.state_id = partner.state_id.id or partner.parent_id.state_id.id
                    rec.zip = partner.zip or partner.parent_id.zip
                    rec.website = partner.website or partner.parent_id.website
                    rec.lang_id = lang and lang[0].id or False
                    rec.function = partner.function or partner.parent_id.function
                    rec.mobile = partner.mobile or partner.parent_id.mobile
                    rec.contact_name = partner.name or partner.parent_id.name
                    rec.partner_name = partner.parent_id.name

        if vals.get('area_sales_manager', False):
            user_id = self.env['res.users'].sudo().browse(vals.get('area_sales_manager'))
            for rec in self:
                new_partner = False
                if vals.get('partner_id'):
                    new_partner = self.env['res.partner'].browse(vals.get('partner_id'))
                rec.add_area_sm_followers(rec.area_sales_manager, user_id, new_partner=new_partner)
        return super(CrmLead, self).write(vals)

    def add_area_sm_followers(self, old_follower, new_follower, new_partner=False):
        old_area_sales_manager = old_follower
        if old_area_sales_manager:
            old_follower = self.env['mail.followers'].search([('res_id', '=', self.id),
                                                              ('res_model', '=', 'crm.lead'),
                                                              ('partner_id', '=', old_area_sales_manager.partner_id.id)])
            if old_follower:
                old_follower.sudo().unlink()
        partner_id = new_follower.partner_id
        new_partner = new_partner and new_partner.id or self.partner_id.id
        customer_subtype_ids = self.env['mail.followers'].search([('res_id', '=', new_partner),
                                                                  ('res_model', '=', 'res.partner'),
                                                                  ('partner_id', '=', partner_id.id)]).subtype_ids
        if not customer_subtype_ids:
            customer_subtype_ids = self.env['mail.message.subtype'].search([('name', '=', 'Discussions'), ('res_model', '=', False)])
        follower_vals = {'res_id': self.id, 'res_model': 'crm.lead',
                         'partner_id': partner_id.id, 'subtype_ids': [(6, 0, customer_subtype_ids.ids)]}
        if partner_id:
            follower = self.env['mail.followers'].search([('res_id', '=', self.id),
                                                          ('res_model', '=', 'crm.lead'),
                                                          ('partner_id', '=', partner_id.id)])
            if not follower:
                self.env['mail.followers'].create(follower_vals)
            else:
                follower.sudo().unlink()
                self.env['mail.followers'].create(follower_vals)
                # follower.write({'subtype_ids': [(6, 0, customer_subtype_ids.ids)]})

    def _onchange_partner_id_values(self, partner_id):
        """ returns the new values when partner_id has changed """
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)

            partner_name = partner.parent_id.name
            if not partner_name and partner.is_company:
                partner_name = partner.name

            user_id = partner.user_id.id or partner.parent_id.user_id.id or False
            partner_email = partner.email
            if partner_email:
                cnt = self.env['res.partner'].search_count([('email', '=', partner_email)])
                if cnt > 1:
                    user_id = False
            return {
                'partner_name': partner_name,
                'contact_name': partner.name if not partner.is_company else False,
                'title': partner.title.id,
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id.id,
                'country_id': partner.country_id.id,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'zip': partner.zip,
                'function': partner.function,
                'website': partner.website,
                'industry_id': partner.industry_id.id or partner.parent_id.industry_id.id,
                'bp_group': partner.bp_group.id or partner.parent_id.bp_group.id,
                'grade_id': partner.grade_id.id or partner.parent_id.grade_id.id,
                'region_id': partner.region_id.id or partner.parent_id.region_id.id,
                'area_sales_manager': partner.area_sales_manager.id or partner.parent_id.area_sales_manager.id,
                'user_id': user_id,
            }
        return {}

    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        """ extract data from lead to create a partner
            :param name : furtur name of the partner
            :param is_company : True if the partner is a company
            :param parent_id : id of the parent partner (False if no parent)
            :returns res.partner record
        """
        res = super(CrmLead, self)._create_lead_partner_data(name, is_company, parent_id)
        res.update({'industry_id': self.industry_id.id,
                    'bp_group': self.bp_group.id,
                    'grade_id': self.grade_id.id,
                    'region_id': self.region_id.id,
                    'area_sales_manager': self.area_sales_manager.id,
                    'user_id': self.user_id.id})
        return res
