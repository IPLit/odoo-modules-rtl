from odoo import api, fields, models, _
from odoo.exceptions import UserError
class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    location_id = fields.Many2one('stock.location', default=False)

    @api.onchange('name')
    def onchange_name(self):
        user = self.env.user
        if user.stock_location_ids:
            location_ids = []
            for location_id in user.stock_location_ids:
                location_ids.append(location_id.id)
            return {'domain': {'location_id': [('id', 'in', location_ids)]}}


    # def write(self,vals):
    #     admin = self.env.user.has_group('base.group_system')
    #     manager = self.env.user.has_group('manufacturing_indent.group_hospital_manager')
    #     if vals and self.state in ['confirm', 'done']:
    #         if admin or manager:
    #             pass
    #         else:
    #             raise UserError(_('You cannot edit the record.'))
    #     return super(StockInventory, self).write(vals)
