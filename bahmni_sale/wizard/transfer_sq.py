from odoo import models,fields, api, _

class SaleAdvancePaymentInv(models.TransientModel):
    _name = 'transfer.sale.quotation.wiz'

    shop_id = fields.Many2one('sale.shop')
    def transfer(self):
        so = self.env['sale.order'].browse(self.env.context.get('active_id'))
        so.write({'shop_id': self.shop_id.id})

