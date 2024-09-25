import json

import requests

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @staticmethod
    def _authenticate_orange_api():
        url = "https://api.orange.com/oauth/v3/token"
        headers = {
            "Authorization": "Basic aFBwOW5sUWJ4S0tVaUx0RzFjZWlhRUE3b0RyMTVBTm06QTM3dFRwMXc3T1pHa1ZNcQ==",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data)
        return response

    def _check_unpaid_customers(self):
        unpaid_invoices = self.env["account.move"].search(
            [
                ("state", "=", "posted"),
                ("amount_residual", ">", 0),
                ("invoice_date_due", "<", fields.date.today()),
            ]
        )
        # mapped pour selectionner a partir de la liste unpaid_invoices les ids de cliens et le mettre dans une liste
        partner_ids = unpaid_invoices.mapped("partner_id")
        response = self._authenticate_orange_api()
        access_token = response.json().get("access_token")
        url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B21650899095/requests"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        for partner_id in partner_ids:
            data = {
                "outboundSMSMessageRequest": {
                    "address": f"tel:+216{partner_id.mobile}",
                    "senderAddress": "tel:+21650899095",
                    "outboundSMSTextMessage": {"message": "Hello!"},
                }
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))

