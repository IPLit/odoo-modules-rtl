from odoo import models, fields,api

class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if not self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
            partner_id = self.env.user.partner_id
            employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
            args.append(('department_id','=',employee_id.department_id.id))

        return super(HrHolidays, self).search(args, offset, limit, order, count)