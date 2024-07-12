# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    level_id = fields.Many2one('employee.level', string='Level')
    # salary_id = fields.Many2one('employee.level',
    #                             related='level_id.salary_level', string='Salary')

    def action_promote(self):
        levels = self.env['employee.level'].filtered(lambda x: x.employee_level)
        print(levels)
