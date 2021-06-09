# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    sap_ref = fields.Char('SAP Reference')
    ref = fields.Char(related='partner_id.ref', string='Customer Reference')
    sequence = fields.Char()
    lead_id = fields.Many2one('crm.lead')
    lead_count = fields.Integer(compute='compute_lead_count')
    origin_ticket_id = fields.Many2one('helpdesk.ticket')

    def compute_lead_count(self):
        for rec in self:
            rec.lead_count = self.env['crm.lead'].search_count([('id', '=', rec.lead_id.id), ('active', '=', False)])

    @api.model
    def create(self, values):
        values['sequence'] = self.env['ir.sequence'].next_by_code('helpdesk.ticket.seq')
        return super(HelpdeskTicket, self).create(values)

    def name_get(self):
        result = []
        for ticket in self:
            result.append((ticket.id, "%s (#%s)" % (ticket.name, ticket.sequence)))
        return result

    def action_view_lead(self):
        self.ensure_one()
        return {
            'name': _('Leads'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'crm.lead',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', '=', self.lead_id.id), ('active', '=', False)],
        }
