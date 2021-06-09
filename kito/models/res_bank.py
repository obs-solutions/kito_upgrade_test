# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    template_bin = fields.Integer(string="Report Template BIN")
    template_account_number = fields.Integer(string="Report Template Account Number")
    template_iban = fields.Char(string="Report Template IBAN")
