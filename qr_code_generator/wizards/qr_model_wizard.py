# -*- coding: utf-8 -*-
from io import BytesIO
from odoo import api, fields, models
try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None


class QRModelWizard(models.TransientModel):
    """Transient model for QR code generating"""
    _name = 'qr.model.wizard'
    _description = 'QR Code Generating model'

    @api.model
    def generate_qr_code(self, input_value):
        """Function for generate qr code"""
        if qrcode and base64 and input_value:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=4,
            )
            qr.add_data(input_value)
            qr.make(fit=True)
            img = qr.make_image()
            temp = BytesIO()
            img.save(temp, format="PNG")
            qr_image = base64.b64encode(temp.getvalue())
            return {'qr_image': qr_image}
        else:
            return 0



