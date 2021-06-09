# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    template_managing_director = fields.Char(string="Report Template Managing Director")
