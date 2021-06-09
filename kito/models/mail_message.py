# -*- coding: utf-8 -*-

from odoo import models, api


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):
        #  Copy message in chatter to Main ticket if incoming mail comes to Archived (merged) ticket
        result = super(MailMessage, self).create(vals)
        if result.model == 'helpdesk.ticket':
            if not self.env['helpdesk.ticket'].browse(result.res_id).active:
                origin_ticket_id = self.env['helpdesk.ticket'].browse(result.res_id).origin_ticket_id
                if origin_ticket_id:
                    result.copy({'res_id': origin_ticket_id.id})
        return result
