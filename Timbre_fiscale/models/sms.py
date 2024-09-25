import json

import requests

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    # @staticmethod
    # def _authenticate_orange_api():
    #     url = "https://api.orange.com/oauth/v3/token"
    #     headers = {
    #         "Authorization": "",
    #         "Content-Type": "application/x-www-form-urlencoded",
    #         "Accept": "application/json",
    #     }
    #     data = {"grant_type": "client_credentials"}
    #
    #     response = requests.post(url, headers=headers, data=data)
    #     return response

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
        # response = self._authenticate_orange_api()
        # access_token = response.json().get("access_token")
        # url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B21622624685/requests"
        # headers = {
        #     "Authorization": f"Bearer {access_token}",
        #     "Content-Type": "application/json",
        # }
        for partner_id in partner_ids:
            # data = {
            #     "outboundSMSMessageRequest": {
            #         "address": f"tel:216{partner_id.mobile}",
            #         "senderAddress": "tel:+21622624685",
            #         "outboundSMSTextMessage": {"message": "Hello!"},
            #     }
            # }
            # response = requests.post(url, headers=headers, data=json.dumps(data))

            sms_composer = self.env["sms.composer"]
            sms_id = sms_composer.create(
                {
                    "res_model": "res.partner",
                    "res_id": partner_id.id,
                    "number_field_name": "mobile",
                    "recipient_single_number_itf": partner_id.mobile,
                    "composition_mode": "comment",
                    "body": f"Hello Mr {partner_id.name} Please give me my money!",
                }
            )
            sms_id.action_send_sms()