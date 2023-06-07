from odoo import fields, models, api
from odoo.tools.float_utils import float_compare

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
	
    shop_id = fields.Many2one('sale.shop', 'Shop')

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        super(AccountInvoice, self)._onchange_partner_id()
        self.onchange_shop_id()

    @api.onchange('shop_id')
    def onchange_shop_id(self):
        if self.shop_id:
            self.payment_term_id = self.shop_id.payment_default_id.id    
