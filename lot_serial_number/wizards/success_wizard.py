# -*- coding: utf-8 -*-
from odoo import models


class SuccessWizard(models.TransientModel):
    """Model for Success message."""
    _name = 'success.wizard'

    def action_return(self):
        """return to importing field of lot/serial number"""
        return {
            'name': 'Success',
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'import.lot.serial.wizard',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'new', }
