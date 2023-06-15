import datetime
import hashlib
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approver_id = fields.Many2one('hr.employee', string="Approver", domain=lambda self: self.get_approver_domain())
    # approver_id = fields.Many2one('hr.employee', string="Approver")
    approval_stage = fields.Integer(default=1)
    department_id = fields.Many2one('account.analytic.account', string="Department", store=True)
    to_approve = fields.Boolean()
    to_approve_po = fields.Boolean()
    show_submit_request = fields.Boolean()
    date_request = fields.Datetime(string="Request Date", compute="_compute_date")
    date_request_deadline = fields.Date(string="Request Deadline", compute="_compute_date")
    state = fields.Selection(
        selection_add=[('to_approve', 'To Approve'), ('disapprove', 'Disapproved'), ('approved', 'Approved')])
    approval_status = fields.Selection(selection=[
        ('po_approval', 'For Approval'),
        ('approved', 'Approved'),
        ('disapprove', 'Disapproved'),
        ('cancel', 'Cancelled')
    ], string='Status')

    disapproval_reason = fields.Char(string="Reason for Disapproval")
    show_request = fields.Char()
    approval_type_id = fields.Many2one('purchase.approval.types')
    approval_id = fields.Many2one('purchase.approval')
    is_approver = fields.Boolean(compute="compute_approver")
    approval_link = fields.Char('Approval link')

    initial_approver_name = fields.Char()

    user_id = fields.Many2one('res.users', 'User', domain=lambda self: [('res_id', 'in', self.env.user.id)])
    check_status = fields.Char(compute='compute_check_status', store=True)
    current_date = fields.Date(default=fields.Datetime.now())

    @api.depends('approval_status', 'state')
    def compute_check_status(self):
        for rec in self:
            if rec.approval_status == 'disapprove' or rec.state == 'disapprove':
                print('state: Disapprove')
                self.submit_for_disapproval()

            elif rec.approval_status == 'approved' or rec.state == 'approved':
                print('state: Approved')
                self.submit_to_final_approver()

    def update_check_status(self):
        self.check_status = False
        self.check_status = True

    def approval_dashboard_link(self):
        action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.order')], limit=1)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        result_1 = re.sub(r'\((.*?)\)', '', str(action)).replace(',', '')
        res = f"{result_1},{action.id}"
        result = re.sub(r'\s*,\s*', ',', res)

        menu = self.env['ir.ui.menu'].search([('action', '=', result)], limit=1)
        params = {
            "action": 1197,
            "model": "purchase.order",
            "view_type": "list",
            "cids": "",
            "menu_id": menu.id
        }

        query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        list_view_url = f"{base_url}/web?debug=1#{query_string}"

        return list_view_url

    def generate_odoo_link(self):
        action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.order')], limit=1)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        result = re.sub(r'\((.*?)\)', '', str(action)).replace(',', '')
        res = f"{result},{action.id}"
        result = re.sub(r'\s*,\s*', ',', res)

        menu = self.env['ir.ui.menu'].search([('action', '=', result)], limit=1)
        params = {
            "id": self.id,
            "action": action.id,
            "model": "purchase.order",
            "view_type": "form",
            "cids": 1,
            "menu_id": menu.id
        }
        query_params = "&".join(f"{key}={value}" for key, value in params.items())
        pr_form_link = f"{base_url}/web#{query_params}"
        return pr_form_link

    def generate_token(self):
        now = datetime.datetime.now()
        token = "{}-{}-{}-{}".format(self.id, self.name, self.env.user.id, now)
        return hashlib.sha256(token.encode()).hexdigest()

    # Initial Approver Sending of Email
    def submit_for_approval(self):
        # Approval Dashboard Link Section
        approval_action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.order')],
                                                                   limit=1)
        approval_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        approval_result_1 = re.sub(r'\((.*?)\)', '', str(approval_action)).replace(',', '')
        approval_res = f"{approval_result_1},{approval_action.id}"
        approval_result = re.sub(r'\s*,\s*', ',', approval_res)

        approval_menu = self.env['ir.ui.menu'].search([('action', '=', approval_result)], limit=1)
        approval_params = {
            "action": 1199,
            "model": "purchase.order",
            "view_type": "list",
            "cids": "",
            "menu_id": approval_menu.id
        }

        approval_query_string = '&'.join([f'{key}={value}' for key, value in approval_params.items()])
        approval_list_view_url = f"{approval_base_url}/web?debug=1#{approval_query_string}"

        # Generate Odoo Link Section
        odoo_action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.order')], limit=1)
        odoo_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        odoo_result = re.sub(r'\((.*?)\)', '', str(odoo_action)).replace(',', '')
        odoo_res = f"{odoo_result},{odoo_action.id}"
        odoo_result = re.sub(r'\s*,\s*', ',', odoo_res)

        odoo_menu = self.env['ir.ui.menu'].search([('action', '=', odoo_result)], limit=1)
        odoo_params = {
            "id": self.id,
            "action": odoo_action.id,
            "model": "purchase.order",
            "view_type": "form",
            "cids": 1,
            "menu_id": odoo_menu.id
        }
        odoo_query_params = "&".join(f"{key}={value}" for key, value in odoo_params.items())
        pr_form_link = f"{odoo_base_url}/web#{odoo_query_params}"

        self.generate_odoo_link()
        self.approval_dashboard_link()

        fetch_getEmailReceiver = 'alex.mercado@teamglac.com'  # self.approver_id.work_email DEFAULT RECEIVER CHANGE IT TO IF YOU WANT ----> IF YOU WANT TO SET AS DEFAULT OR ONLY ONE ##
        self.sendingEmail(fetch_getEmailReceiver, pr_form_link, approval_list_view_url)

        self.write({
            'approval_status': 'po_approval',
            'state': 'to_approve',
            'to_approve': True,
            'show_submit_request': False
        })

    def sendingEmail(self, fetch_getEmailReceiver, pr_form_link, approval_list_view_url):
        sender = 'noreply@teamglac.com'
        host = "192.168.1.114"
        port = 25
        username = "noreply@teamglac.com"
        password = "noreply"

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        token = self.generate_token()

        approval_url = "{}/request/approve/{}".format(base_url, token)
        disapproval_url = "{}/request/disapprove/{}".format(base_url, token)

        self.write({'approval_link': token})

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = fetch_getEmailReceiver
        msg['Subject'] = 'Odoo Purchasing Mailer - Purchase Order For Approval [' + self.name + ']'

        html_content = """
            <html>
            <head>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }

                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background-color: #dddddd;
                    }

                </style>
            </head>
            <body>"""

        html_content += f"""
            <br></br>
                <dd>Requested by: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
                <dd>Date Requested: &nbsp;&nbsp;{self.date_approve if self.date_approve != False else ""}</dd>
                <dd>Vendor: &nbsp;&nbsp;{self.partner_id.name if self.partner_id.name != False else ""}</dd>
                <dd>Currency: &nbsp;&nbsp;{self.currency_id.name if self.currency_id.name != False else ""}</dd>
                <dd>Source Document: &nbsp;&nbsp;{self.origin if self.origin != False else ""}</dd>
            <br></br>
                <span><b>ITEMS REQUESTED</b></span>
            <br></br>
        """
        #
        # html_content += f"""
        # <dt><b>{self.name}</b></dt>
        # <br></br>
        # <dd style="display: none;">{self.approver_count}</dd>
        #
        # <dd>Requested by: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
        # <dd>Date Requested: &nbsp;&nbsp;{self.ordering_date if self.ordering_date != False else ""}</dd>
        # """

        html_content += """
        <br></br>
        <table>
                    <tr>
                        <th>Product</th>
                        <th>Description</th>
                        <th>Scheduled Date</th>
                        <th>Analytic Account</th>
                        <th>Quantity</th>
                        <th>Received</th>
                        <th>UoM</th>
                        <th>Unit Price</th>
                        <th>Taxes</th>
                        <th>Subtotal</th>
                    </tr>
                    """

        for line in self.order_line:
            html_content += f"""
                    <tr>
                        <td>{line.product_id.name}</td>
                        <td>{line.name}</td>
                        <td>{line.date_planned}</td>
                        <td>{line.account_analytic_id.name}</td>
                        <td>{line.product_qty}</td>
                        <td>{line.qty_received}</td>
                        <td>{line.product_uom.name}</td>
                        <td>{line.price_unit}</td>
                        <td>{line.taxes_id.name if line.taxes_id.name != False else ""}</td>
                        <td>{line.price_subtotal}&nbsp;{self.currency_id.name if self.currency_id.name != False else ""}</td>
                    </tr>
        """

        html_content += f"""
            </table>

            </body>
            <br></br>
            <br></br>
            <br></br>
            <span style="font-style: italic;";><a href="{approval_url}"  style="color: green;">APPROVE</a> / <a href="{disapproval_url}"  style="color: red;">DISAPPROVE</a> / <a href="{pr_form_link}"  style="color: blue;">ODOO PO FORM
            </a> / <a href="{approval_list_view_url}">ODOO APPROVAL DASHBOARD</a></span>

            </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        try:
            smtpObj = smtplib.SMTP(host, port)
            smtpObj.login(username, password)
            smtpObj.sendmail(sender, fetch_getEmailReceiver, msg.as_string())

            msg = "Successfully sent email"
            print(msg)
            return {
                'success': {
                    'title': 'Successfully email sent!',
                    'message': f'{msg}'}
            }
        except Exception as e:
            msg = f"Error: Unable to send email: {str(e)}"
            print(msg)
            return {
                'warning': {
                    'title': 'Error: Unable to send email!',
                    'message': f'{msg}'}
            }

        # Next Approver Sending of Email

    def submit_to_next_approver(self):
        # Approval Dashboard Link Section
        approval_action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.order')],
                                                                   limit=1)
        approval_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        approval_result_1 = re.sub(r'\((.*?)\)', '', str(approval_action)).replace(',', '')
        approval_res = f"{approval_result_1},{approval_action.id}"
        approval_result = re.sub(r'\s*,\s*', ',', approval_res)

        approval_menu = self.env['ir.ui.menu'].search([('action', '=', approval_result)], limit=1)
        approval_params = {
            "action": 1199,
            "model": "purchase.order",
            "view_type": "list",
            "cids": "",
            "menu_id": approval_menu.id
        }

        approval_query_string = '&'.join([f'{key}={value}' for key, value in approval_params.items()])
        approval_list_view_url = f"{approval_base_url}/web?debug=1#{approval_query_string}"

        # Generate Odoo Link Section
        odoo_action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.order')], limit=1)
        odoo_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        odoo_result = re.sub(r'\((.*?)\)', '', str(odoo_action)).replace(',', '')
        odoo_res = f"{odoo_result},{odoo_action.id}"
        odoo_result = re.sub(r'\s*,\s*', ',', odoo_res)

        odoo_menu = self.env['ir.ui.menu'].search([('action', '=', odoo_result)], limit=1)
        odoo_params = {
            "id": self.id,
            "action": odoo_action.id,
            "model": "purchase.order",
            "view_type": "form",
            "cids": 1,
            "menu_id": odoo_menu.id
        }
        odoo_query_params = "&".join(f"{key}={value}" for key, value in odoo_params.items())
        pr_form_link = f"{odoo_base_url}/web#{odoo_query_params}"

        self.generate_odoo_link()
        self.approval_dashboard_link()

        fetch_getEmailReceiver = 'alex.mercado@teamglac.com'  # self.approver_id.work_email DEFAULT RECEIVER CHANGE IT TO IF YOU WANT ----> IF YOU WANT TO SET AS DEFAULT OR ONLY ONE ##
        self.sending_email_to_next_approver(fetch_getEmailReceiver, pr_form_link, approval_list_view_url)

        self.write({
            'approval_status': 'po_approval',
            'state': 'to_approve',
            'to_approve': True,
            'show_submit_request': False
        })

    def sending_email_to_next_approver(self, fetch_getEmailReceiver, pr_form_link, approval_list_view_url):
        sender = 'noreply@teamglac.com'
        host = "192.168.1.114"
        port = 25
        username = "noreply@teamglac.com"
        password = "noreply"

        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        token = self.generate_token()

        approval_url = "{}/request/approve/{}".format(base_url, token)
        disapproval_url = "{}/request/disapprove/{}".format(base_url, token)

        self.write({'approval_link': token})

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = fetch_getEmailReceiver  # Change this to next approvers email address
        msg['Subject'] = 'Odoo Purchasing Mailer - Purchase Order For Approval NEXT APPROVER[' + self.name + ']'

        html_content = """
            <html>
            <head>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }

                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background-color: #dddddd;
                    }

                </style>
            </head>
            <body>"""

        html_content += f"""
            <br></br>
                <dd>Purchase Representative: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
                <dd>Confirmation Date: &nbsp;&nbsp;{self.date_approve if self.date_approve != False else ""}</dd>
            <br></br>
            <br></br>
                <dd>Vendor: &nbsp;&nbsp;{self.partner_id.name if self.partner_id.name != False else ""}</dd>
                <dd>Currency: &nbsp;&nbsp;{self.currency_id.name if self.currency_id.name != False else ""}</dd>
                <dd>Source Document: &nbsp;&nbsp;{self.origin if self.origin != False else ""}</dd>
            <br></br>
                <span><b>ITEMS REQUESTED</b></span>
            <br></br>
        """
        html_content += """
        <br></br>
        <table>
                    <tr>
                        <th>Product</th>
                        <th>Description</th>
                        <th>Scheduled Date</th>
                        <th>Analytic Account</th>
                        <th>Quantity</th>
                        <th>Received</th>
                        <th>UoM</th>
                        <th>Unit Price</th>
                        <th>Taxes</th>
                        <th>Subtotal</th>
                    </tr>
                    """

        for line in self.order_line:
            html_content += f"""
                    <tr>
                        <td>{line.product_id.name}</td>
                        <td>{line.name}</td>
                        <td>{line.date_planned}</td>
                        <td>{line.account_analytic_id.name}</td>
                        <td>{line.product_qty}</td>
                        <td>{line.qty_received}</td>
                        <td>{line.product_uom.name}</td>
                        <td>{line.price_unit}</td>
                        <td>{line.taxes_id.name if line.taxes_id.name != False else ""}</td>
                        <td>{line.price_subtotal}&nbsp;{self.currency_id.name if self.currency_id.name != False else ""}</td>
                    </tr>
        """

        html_content += f"""
            </table>

            </body>
            <br></br>
            <br></br>
            <br></br>
            <span style="font-style: italic;";><a href="{approval_url}"  style="color: green;">APPROVE</a> / <a href="{disapproval_url}"  style="color: red;">DISAPPROVE</a> / <a href="{pr_form_link}"  style="color: blue;">ODOO PO FORM
            </a> / <a href="{approval_list_view_url}">ODOO APPROVAL DASHBOARD</a></span>

            </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        try:
            smtpObj = smtplib.SMTP(host, port)
            smtpObj.login(username, password)
            smtpObj.sendmail(sender, fetch_getEmailReceiver, msg.as_string())

            msg = "Successfully sent email"
            print(msg)
            return {
                'success': {
                    'title': 'Successfully email sent!',
                    'message': f'{msg}'}
            }
        except Exception as e:
            msg = f"Error: Unable to send email: {str(e)}"
            print(msg)
            return {
                'warning': {
                    'title': 'Error: Unable to send email!',
                    'message': f'{msg}'}
            }

    # PO is DISAPPROVED
    def submit_for_disapproval(self):
        # Generate Odoo Link Section
        odoo_action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.order')], limit=1)
        odoo_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        odoo_result = re.sub(r'\((.*?)\)', '', str(odoo_action)).replace(',', '')
        odoo_res = f"{odoo_result},{odoo_action.id}"
        odoo_result = re.sub(r'\s*,\s*', ',', odoo_res)

        odoo_menu = self.env['ir.ui.menu'].search([('action', '=', odoo_result)], limit=1)
        odoo_params = {
            "id": self.id,
            "action": odoo_action.id,
            "model": "purchase.order",
            "view_type": "form",
            "cids": 1,
            "menu_id": odoo_menu.id
        }
        odoo_query_params = "&".join(f"{key}={value}" for key, value in odoo_params.items())
        PO_form_link = f"{odoo_base_url}/web#{odoo_query_params}"

        self.generate_odoo_link()

        fetch_getEmailReceiver = 'alex.mercado@teamglac.com'  # self.approver_id.work_email DEFAULT RECEIVER CHANGE IT TO IF YOU WANT ----> IF YOU WANT TO SET AS DEFAULT OR ONLY ONE ##
        self.send_disapproval_email(fetch_getEmailReceiver, PO_form_link)

    def send_disapproval_email(self, fetch_getEmailReceiver, PO_form_link):
        sender = 'noreply@teamglac.com'
        host = "192.168.1.114"
        port = 25
        username = "noreply@teamglac.com"
        password = "noreply"

        token = self.generate_token()
        self.write({'approval_link': token})

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = fetch_getEmailReceiver
        msg['Subject'] = 'Odoo Purchasing Mailer - Purchase Order Disapproved [' + self.name + ']'

        html_content = """
            <html>
            <head>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }

                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background-color: #dddddd;
                    }

                </style>
            </head>
            <body>"""

        html_content += f"""
        <dt><b>{self.name}</b></dt>
            <br></br>
                <dd>Purchase Representative: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
                <dd>Confirmation Date: &nbsp;&nbsp;{self.date_approve if self.date_approve != False else ""}</dd>
                <dd>Disapproved by: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
                <dd>Disapproval date: &nbsp;&nbsp;{self.current_date if self.current_date != False else ""}</dd>
                <dd>Reason for Disapproval: &nbsp;&nbsp;{self.disapproval_reason if self.disapproval_reason != False else ""}</dd>
            <br></br>
            <br></br>
                <dd>Vendor: &nbsp;&nbsp;{self.partner_id.name if self.partner_id.name != False else ""}</dd>
                <dd>Currency: &nbsp;&nbsp;{self.currency_id.name if self.currency_id.name != False else ""}</dd>
                <dd>Source Document: &nbsp;&nbsp;{self.origin if self.origin != False else ""}</dd>
            <br></br>
                <span><b>ITEMS REQUESTED</b></span>
            <br></br>
        """

        html_content += """
        <br></br>
        <table>
                    <tr>
                        <th>Product</th>
                        <th>Description</th>
                        <th>Scheduled Date</th>
                        <th>Analytic Account</th>
                        <th>Quantity</th>
                        <th>Received</th>
                        <th>UoM</th>
                        <th>Unit Price</th>
                        <th>Taxes</th>
                        <th>Subtotal</th>
                    </tr>
                    """

        for line in self.order_line:
            html_content += f"""
                    <tr>
                        <td>{line.product_id.name}</td>
                        <td>{line.name}</td>
                        <td>{line.date_planned}</td>
                        <td>{line.account_analytic_id.name}</td>
                        <td>{line.product_qty}</td>
                        <td>{line.qty_received}</td>
                        <td>{line.product_uom.name}</td>
                        <td>{line.price_unit}</td>
                        <td>{line.taxes_id.name if line.taxes_id.name != False else ""}</td>
                        <td>{line.price_subtotal}&nbsp;{self.currency_id.name if self.currency_id.name != False else ""}</td>
                    </tr>
        """

        html_content += f"""
            </table>
            </body>
            <br></br>
            <br></br>
            <br></br>
            <span> <a href="{PO_form_link}" style="color: blue;">ODOO PR FORM</span>

            </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        try:
            smtpObj = smtplib.SMTP(host, port)
            smtpObj.login(username, password)
            smtpObj.sendmail(sender, fetch_getEmailReceiver, msg.as_string())

            msg = "Successfully sent email"
            print(msg)
            return {
                'success': {
                    'title': 'Successfully email sent!',
                    'message': f'{msg}'}
            }
        except Exception as e:
            msg = f"Error: Unable to send email: {str(e)}"
            print(msg)
            return {
                'warning': {
                    'title': 'Error: Unable to send email!',
                    'message': f'{msg}'}
            }

    # PO is approved by final approver
    def submit_to_final_approver(self):
        fetch_getEmailReceiver = 'alex.mercado@teamglac.com'  # self.approver_id.work_email DEFAULT RECEIVER CHANGE IT TO IF YOU WANT ----> IF YOU WANT TO SET AS DEFAULT OR ONLY ONE ##
        self.send_to_final_approver_email(fetch_getEmailReceiver)

    def send_to_final_approver_email(self, fetch_getEmailReceiver):
        sender = 'noreply@teamglac.com'
        host = "192.168.1.114"
        port = 25
        username = "noreply@teamglac.com"
        password = "noreply"

        token = self.generate_token()
        self.write({'approval_link': token})

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = fetch_getEmailReceiver
        msg['Subject'] = 'Odoo Purchasing Mailer - Purchase Order Approved [' + self.name + ']'

        html_content = """
            <html>
            <head>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 100%;
                    }

                    th, td {
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                    }

                    th {
                        background-color: #dddddd;
                    }

                </style>
            </head>
            <body>"""

        html_content += f"""
                <dt><b>{self.name}</b></dt>
                <br></br>
                <dd>Purchase Representative: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
                <dd>Confirmation Date: &nbsp;&nbsp;{self.date_approve if self.date_approve != False else ""}</dd>
                """

        html_content += f"""
                    <dd>{self.initial_approver_name}</dd>
                    <dd>Final Approval by: &nbsp;&nbsp;{self.approver_id.name if self.approver_id.name != False else ""}</dd>
                    <dd>Final Approval date: &nbsp;&nbsp;{self.current_date if self.current_date != False else ""}</dd>
                    """
        #
        # if self.approver_count >= 2:
        #     html_content += f"""
        #             <dd>Second Approval: &nbsp;&nbsp;{self.second_approver_id.name if self.second_approver_id.name != False else ""}</dd>
        #             <dd>Second Approval date: &nbsp;&nbsp;{self.current_date if self.current_date != False else ""}</dd>
        #             """
        #
        # if self.approver_count >= 3:
        #     html_content += f"""
        #            <dd>Third Approval: &nbsp;&nbsp;{self.third_approver_id.name if self.third_approver_id.name != False else ""}</dd>
        #            <dd>Third Approval date: &nbsp;&nbsp;{self.current_date if self.current_date != False else ""}</dd>
        #            """
        #
        # if self.approver_count >= 4:
        #     html_content += f"""
        #             <dd>Fourth Approval: &nbsp;&nbsp;{self.fourth_approver_id.name if self.fourth_approver_id.name != False else ""}</dd>
        #             <dd>Fourth Approval date: &nbsp;+&nbsp;{self.current_date if self.current_date != False else ""}</dd>
        #             """
        #
        # if self.approver_count >= 5:
        #     html_content += f"""
        #             <dd>Fifth Approval: &nbsp;&nbsp;{self.fifth_approver_id.name if self.fifth_approver_id.name != False else ""}</dd>
        #             <dd>Fifth Approval date: &nbsp;&nbsp;{self.current_date if self.current_date != False else ""}</dd>
        #             """

        html_content += f"""
                <br></br>
                <br></br>
                <dd>Vendor: &nbsp;&nbsp;{self.partner_id.name if self.partner_id.name != False else ""}</dd>
                <dd>Currency: &nbsp;&nbsp;{self.currency_id.name if self.currency_id.name != False else ""}</dd>
                <dd>Source Document: &nbsp;&nbsp;{self.origin if self.origin != False else ""}</dd>
                <br></br>
                <span><b>ITEMS REQUESTED</b></span>
                <br></br>
                """

        html_content += """
        <br></br>
        <table>
                    <tr>
                        <th>Product</th>
                        <th>Description</th>
                        <th>Scheduled Date</th>
                        <th>Analytic Account</th>
                        <th>Quantity</th>
                        <th>Received</th>
                        <th>UoM</th>
                        <th>Unit Price</th>
                        <th>Taxes</th>
                        <th>Subtotal</th>
                    </tr>
                    """

        for line in self.order_line:
            html_content += f"""
                    <tr>
                        <td>{line.product_id.name}</td>
                        <td>{line.name}</td>
                        <td>{line.date_planned}</td>
                        <td>{line.account_analytic_id.name}</td>
                        <td>{line.product_qty}</td>
                        <td>{line.qty_received}</td>
                        <td>{line.product_uom.name}</td>
                        <td>{line.price_unit}</td>
                        <td>{line.taxes_id.name if line.taxes_id.name != False else ""}</td>
                        <td>{line.price_subtotal}&nbsp;{self.currency_id.name if self.currency_id.name != False else ""}</td>
                    </tr>
        """

        html_content += f"""
            </table>
            </body>
            <br></br>
            </html>
        """

        msg.attach(MIMEText(html_content, 'html'))

        try:
            smtpObj = smtplib.SMTP(host, port)
            smtpObj.login(username, password)
            smtpObj.sendmail(sender, fetch_getEmailReceiver, msg.as_string())

            msg = "Successfully sent email"
            print(msg)
            return {
                'success': {
                    'title': 'Successfully email sent!',
                    'message': f'{msg}'}
            }
        except Exception as e:
            msg = f"Error: Unable to send email: {str(e)}"
            print(msg)
            return {
                'warning': {
                    'title': 'Error: Unable to send email!',
                    'message': f'{msg}'}
            }

    def _compute_date(self):
        for rec in self:
            rec.date_request = rec.requisition_id.ordering_date
            rec.date_request_deadline = rec.requisition_id.date_end

    @api.onchange('department_id', 'approval_stage')
    def get_approver_domain(self):
        for rec in self:
            domain = []

            res = self.env["department.approvers"].search(
                [("dept_name", "=", rec.department_id.id), ("approval_type.name", '=', 'Purchase Orders')])

            if rec.department_id and rec.approval_stage == 1:
                try:
                    approver_dept = [x.first_approver.id for x in res.set_first_approvers]
                    rec.approver_id = approver_dept[0]
                    domain.append(('id', '=', approver_dept))

                except IndexError:
                    raise UserError(_("No Approvers set for {}!").format(rec.department_id.name))

            elif rec.department_id and rec.approval_stage == 2:
                approver_dept = [x.second_approver.id for x in res.set_second_approvers]
                rec.approver_id = approver_dept[0]
                domain.append(('id', '=', approver_dept))

            elif rec.department_id and rec.approval_stage == 3:
                approver_dept = [x.third_approver.id for x in res.set_third_approvers]
                rec.approver_id = approver_dept[0]
                domain.append(('id', '=', approver_dept))

            elif rec.department_id and rec.approval_stage == 4:
                approver_dept = [x.fourth_approver.id for x in res.set_fourth_approvers]
                rec.approver_id = approver_dept[0]
                domain.append(('id', '=', approver_dept))

            elif rec.department_id and rec.approval_stage == 5:
                approver_dept = [x.fifth_approver.id for x in res.set_fifth_approvers]
                rec.approver_id = approver_dept[0]
                domain.append(('id', '=', approver_dept))

            else:
                domain = []

            return {'domain': {'approver_id': domain}}

    def compute_approver(self):
        # self.approve_request()
        test1 = self.initial_approver_name
        print(test1)
        for rec in self:
            if self.env.user.name == rec.approver_id.name:
                # print('True')
                # print(self.env.user.name, ' | ', rec.approver_id.name)
                self.update({
                    'is_approver': True,
                })
            else:
                self.update({
                    'is_approver': False,
                })

    @api.depends('approval_stage')
    def approve_request(self):
        for rec in self:
            res = self.env["department.approvers"].search(
                [("dept_name", "=", rec.department_id.id), ("approval_type.name", '=', 'Purchase Orders')])

            if rec.approver_id and rec.approval_stage < res.no_of_approvers:
                if rec.approval_stage == 1:
                    approver_dept = [x.second_approver.id for x in res.set_second_approvers]
                    self.submit_to_next_approver()

                    if self.initial_approver_name is None:
                        raise UserError('must set first')
                    else:
                        self.initial_approver_name = rec.approver_id.name

                    print('received by 2nd approver and email sent to next approver')
                    self.write({
                        'approver_id': approver_dept[0]
                    })
                    # rec.initial_approver_name = first_approver_name

                    # return rec.approver_dept

                if rec.approval_stage == 2:
                    approver_dept = [x.third_approver.id for x in res.set_third_approvers]
                    self.submit_to_next_approver()
                    print(rec.approver_id, rec.approval_stage, res.no_of_approvers)

                    print('received by 3rd approver and email sent to next approver')

                    self.write({
                        'approver_id': approver_dept[0]
                    })
                if rec.approval_stage == 3:
                    approver_dept = [x.fourth_approver.id for x in res.set_fourth_approvers]
                    self.submit_to_next_approver()

                    self.write({
                        'approver_id': approver_dept[0]
                    })
                if rec.approval_stage == 4:
                    self.submit_to_next_approver()
                    approver_dept = [x.fifth_approver.id for x in res.set_fifth_approvers]

                    self.write({
                        'approver_id': approver_dept[0]
                    })
                rec.approval_stage += 1
            else:
                self.write({
                    'state': 'approved',
                    'approval_status': 'approved'
                })
                print('end of method approved request')

    def button_cancel(self):
        for order in self:
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(
                        _("Unable to cancel this purchase order. You must first cancel the related vendor bills."))

        self.write({'state': 'cancel',
                    'approval_status': 'cancel'})
