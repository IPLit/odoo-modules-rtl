from odoo import api, fields, models, _
from odoo.exceptions import UserError
class StockScrap(models.Model):
    _inherit = 'stock.scrap'
    product_id = fields.Many2one('product.product', default=False)
    location_id = fields.Many2one('stock.location', default=False)
    location_id1 = fields.Many2one('stock.location', default=False)
    # check_is_admin = fields.Boolean(compute='get_admin')
    state = fields.Selection([
        ('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'),
        ('rejected', 'Rejected')], string='Status', default="draft")

    # @api.depends('check_is_admin')
    # def get_admin(self):
    #     admin = self.env.user.has_group('base.group_system')
    #     manager = self.env.user.has_group('manufacturing_indent.group_hospital_manager')
    #     print('################')
    #     if admin or manager:
    #         print('@@@@@@@@@@@@@@@@@@')
    #         self.check = True
    @api.onchange('product_id')
    def _onchange_product_id(self):
        user=self.env.user
        if user.stock_location_ids:
            location_ids = []
            for location_id in user.stock_location_ids:
                location_ids.append(location_id.id)
            return {'domain': {'location_id': [('id', 'in', location_ids)]}}

    @api.multi
    def do_scrap(self):
        for scrap in self:
            moves = scrap._get_origin_moves() or self.env['stock.move']
            move = self.env['stock.move'].create(scrap._prepare_move_values())
            if move.product_id.type == 'product':
                quants = self.env['stock.quant'].quants_get_preferred_domain(
                    move.product_qty, move,
                    domain=[
                        ('qty', '>', 0),
                        ('lot_id', '=', self.lot_id.id),
                        ('package_id', '=', self.package_id.id)],
                    preferred_domain_list=scrap._get_preferred_domain())
                if any([not x[0] for x in quants]):
                    raise UserError(_('You cannot scrap a move without having available stock for %s. You can correct it with an inventory adjustment.') % move.product_id.name)
        self.write({'state': 'to_approve'})
        return True

    @api.multi
    def do_scrap_transfer(self):
        for scrap in self:
            moves = scrap._get_origin_moves() or self.env['stock.move']
            move = self.env['stock.move'].create(scrap._prepare_move_values())
            if move.product_id.type == 'product':
                quants = self.env['stock.quant'].quants_get_preferred_domain(
                    move.product_qty, move,
                    domain=[
                        ('qty', '>', 0),
                        ('lot_id', '=', self.lot_id.id),
                        ('package_id', '=', self.package_id.id)],
                    preferred_domain_list=scrap._get_preferred_domain())
                if any([not x[0] for x in quants]):
                    raise UserError(_('You cannot scrap a move without having available stock for %s. You can correct it with an inventory adjustment.') % move.product_id.name)
                self.env['stock.quant'].quants_reserve(quants, move)
            move.action_done()
            scrap.write({'move_id': move.id})
            moves.recalculate_move_state()
        return True

    def button_approve(self):
        self.do_scrap_transfer()
        self.write({'state': 'approved'})


    def button_reject(self):
        self.write({'state': 'rejected'})
