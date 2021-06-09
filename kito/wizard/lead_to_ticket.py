# -*- coding: utf-8 -*-

from odoo import models, _


class CrmLeadConvert2Ticket(models.TransientModel):

    _inherit = "crm.lead.convert2ticket"

    def action_lead_to_helpdesk_ticket(self):
        self.ensure_one()
        # get the lead to transform
        lead = self.lead_id
        #partner_id = lead._find_matching_partner(email_only=False)
        partner_id = self.partner_id.id
        if not partner_id and (lead.partner_name or lead.contact_name):
            lead.handle_partner_assignment(create_missing=True)
            partner_id = lead.partner_id.id
        # create new helpdesk.ticket
        vals = {
            "name": lead.name,
            "description": lead.description,
            "email": lead.email_from,
            "team_id": self.team_id.id,
            "ticket_type_id": self.ticket_type_id.id,
            "partner_id": partner_id,
            "user_id": None,
            "lead_id": lead.id
        }
        ticket = self.env['helpdesk.ticket'].create(vals)
        # move the mail thread
        lead.message_change_thread(ticket)
        # move attachments
        attachments = self.env['ir.attachment'].search([('res_model', '=', 'crm.lead'), ('res_id', '=', lead.id)])
        attachments.sudo().write({'res_model': 'helpdesk.ticket', 'res_id': ticket.id})
        # archive the lead
        lead.write({'active': False})
        # return the action to go to the form view of the new Ticket
        view = self.env.ref('helpdesk.helpdesk_ticket_view_form')
        return {
            'name': _('Ticket created'),
            'view_mode': 'form',
            'view_id': view.id,
            'res_model': 'helpdesk.ticket',
            'type': 'ir.actions.act_window',
            'res_id': ticket.id,
            'context': self.env.context
        }
