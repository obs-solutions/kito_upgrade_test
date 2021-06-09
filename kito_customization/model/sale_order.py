# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_warning_appeared = fields.Boolean(string='Stock Qty. running low')

    @api.onchange('product_uom_qty', 'product_id')
    def check_product_warning_qty(self):
        '''
            Method for check warning qty based on the product available qty
        '''
        if self.product_id.warning_qty:
            sales_forcast = self.product_id.qty_available - self.product_uom_qty
            if sales_forcast <= self.product_id.warning_qty:
                self.is_warning_appeared = True
                return {'warning': {
                    'title': _("Warning"),
                    'message': _("Warning - the product {} is about to sell out for a longer period of time".format(
                        self.product_id.name))
                }}
            else:
                self.is_warning_appeared = False

    @api.onchange('product_id')
    def _onchange_product_id_set_route_domain(self):
        self.route_id = False
        domain = [('id', 'in', self.product_id.route_ids.ids)]
        return {
            'domain': {'route_id': domain},
        }


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warning_text = fields.Text(string="Warning", copy=False)

    @api.depends('order_line')
    def _compute_warning_qty_lines(self):
        warning_lines = self.order_line.filtered(lambda line: line.is_warning_appeared)
        if warning_lines:
            self.warning_text = 'Warning - Over Sell Products found in order line.!'
        else:
            self.warning_text = ''

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        super().onchange_partner_id()
        if self.partner_id.grade_id.pricelist_id:
            self.update({'pricelist_id': self.partner_id.grade_id.pricelist_id})
