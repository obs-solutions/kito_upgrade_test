# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    warning_qty = fields.Float('Warning Qty', compute='_compute_warning_qty',
                               inverse='_set_warning_qty', store=True, copy=True)

    lifting_capacity_gt = fields.Char(string='Lifting Capacity GT', copy=True)
    category_gt = fields.Char(string='Category GT', copy=True)
    lifting_height = fields.Float(string='Lifting Height', copy=True)
    legnth_of_headchain = fields.Float(string='Length Of Headchain', copy=True)
    legnth_of_control_cable = fields.Float(string='Length Of Control Cable', copy=True)
    color = fields.Char(string='Painting/Color/Surface', copy=True)
    push_button_switch = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Push Button Switch', copy=True)
    predecessor_id = fields.Many2one('product.template', string='Predecessor', copy=True)
    successor_id = fields.Many2one('product.template', string='Successor', copy=True)

    @api.constrains('successor_id')
    def _check_successor_recursion(self):
        if not self._check_recursion('successor_id'):
            raise ValidationError(_('You cannot create recursive Successor.'))
        return True

    @api.constrains('predecessor_id')
    def _check_predecessor_recursion(self):
        if not self._check_recursion('predecessor_id'):
            raise ValidationError(_('You cannot create recursive Predecessor.'))
        return True

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
