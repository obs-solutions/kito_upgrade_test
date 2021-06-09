# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartnerGrade(models.Model):
    _inherit = 'res.partner.grade'

    pricelist_id = fields.Many2one('product.pricelist', string='Grade Pricelist')
