# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    warning_qty = fields.Float('Warning Qty', compute='_compute_warning_qty',
                               inverse='_set_warning_qty', store=True, copy=True)

    @api.depends('product_variant_ids', 'product_variant_ids.warning_qty')
    def _compute_warning_qty(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.warning_qty = template.product_variant_ids.warning_qty
        for template in (self - unique_variants):
            template.warning_qty = False

    def _set_warning_qty(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.warning_qty = template.warning_qty


class ProductProdcut(models.Model):
    _inherit = 'product.product'

    warning_qty = fields.Float(string='Warning Qty', copy=True)
