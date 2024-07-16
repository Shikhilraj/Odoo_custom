# -*- coding: utf-8 -*-
from odoo.http import request
from odoo import http
from werkzeug.exceptions import Forbidden
import hmac
import logging
import pprint

_logger = logging.getLogger(__name__)


class PayUController(http.Controller):
    _return_url = '/payment/payu/return'
    _failure_url = '/payment/payu/failure'

    @http.route(_return_url, type='http', auth='public',
                methods=['GET', 'POST'], csrf=False, save_session=False)
    def payu_return_from_checkout(self, **data):
        """Process the notification data sent by payu after redirection."""

        _logger.info("handling redirection from PayU with data:\n%s",
                     pprint.pformat(data))
        # Check the integrity of the notification
        tx_sudo = (request.env['payment.transaction'].
                   sudo()._get_tx_from_notification_data('payu', data))
        self._verify_notification_signature(data, tx_sudo)

        # Handle the notification data
        tx_sudo._handle_notification_data('payu', data)
        return request.redirect('/payment/status')

    @staticmethod
    def _verify_notification_signature(notification_data, tx_sudo):
        """ Check that the received signature matches the expected one. """
        # Retrieve the received signature from the data
        received_signature = notification_data.get('hash')
        if not received_signature:
            _logger.warning("received notification with missing signature")
            raise Forbidden()

        # Compare the received signature with the expected signature
        expected_signature = tx_sudo.provider_id._payu_generate_sign(
            notification_data, incoming=True
        )
        if not hmac.compare_digest(received_signature, expected_signature):
            _logger.warning("received notification with invalid signature")
            raise Forbidden()

