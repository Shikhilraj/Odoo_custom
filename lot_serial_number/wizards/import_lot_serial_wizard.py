# -*- coding: utf-8 -*-
from odoo import fields, models
import openpyxl
import base64
from io import BytesIO
from odoo.exceptions import UserError


class ImportLotSerialWizard(models.TransientModel):
    """Wizard for import lot/serial number to products"""
    _name = "import.lot.serial.wizard"

    file = fields.Binary(string="File", required=True)

    def import_lot_serial(self):
        """method for import lot/serial number to product"""
        try:
            wb = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file)), read_only=True)
            ws = wb.active
            for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,
                                       max_col=None, values_only=True):
                if record[0] is None or record[1] is None:
                    continue
                search_product = self.env['product.product'].search(
                    [('name', '=', record[0])])
                if not search_product:
                    search_product = (self.env['product.product'].
                                      create({'name': record[0]}))
                    self.env['stock.lot'].create({
                        'name': record[1],
                        'product_id': search_product.id})
                search_lot = (self.env['stock.lot'].
                              search([('name', '=', record[1]),
                                      ('product_id', '=',
                                       search_product.id)]))
                if not search_lot:
                    self.env['stock.lot'].create({
                        'name': record[1],
                        'product_id': search_product.id
                    })
            return {
                'name': 'Success',
                'view_type': 'form',
                "view_mode": 'form',
                'res_model': 'success.wizard',
                'type': 'ir.actions.act_window',
                'context': {'default_name': 'Success'},
                'target': 'new', }
        except:
            raise UserError('Please insert a valid file')
