# -*- coding: utf-8 -*-
from odoo import fields, models


class EmployeeLevel(models.Model):
    _name = 'employee.level'
    _description = 'Employee Level'

    employee_level = fields.Char(string='Level')
    salary_level = fields.Float(string='Salary', default=0)
    highest = fields.Boolean(default=False, string='Highest')

