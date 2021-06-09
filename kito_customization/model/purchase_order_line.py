# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    order_line_number = fields.Integer(compute='_compute_get_number', store=True, group_operator=False)

    @api.depends('sequence', 'order_id')
    def _compute_get_number(self):
        for order in self.mapped('order_id'):
            order_line_number = 1
            for line in order.order_line:
                if line.display_type in ['line_section', 'line_note']:
                    continue
                line.order_line_number = order_line_number
                order_line_number += 1
