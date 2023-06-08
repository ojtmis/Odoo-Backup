import datetime
import hashlib
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.requisition"
    approver_id = fields.Many2one('hr.employee', string="Approver", domain=lambda self: self.get_approver_domain())
    approval_stage = fields.Integer(default=1)
    department_id = fields.Many2one('account.analytic.account', string="Department", store=True)
    to_approve = fields.Boolean()
    to_approve_po = fields.Boolean()
    show_submit_request = fields.Boolean()
    state = fields.Selection(
        selection_add=[('to_approve', 'To Approve'), ('open',), ('approved', 'Approved'),
                       ('disapprove', 'Disapproved')])
    state_blanket_order = fields.Selection(
        selection_add=[('to_approve', 'To Approve'), ('open',), ('approved', 'Approved'),
                       ('disapprove', 'Disapproved')])
    approval_status = fields.Selection(selection=[
        ('pr_approval', 'For Approval'),
        ('approved', 'Approved'),
        ('disapprove', 'Disapproved'),
        ('cancel', 'Cancelled')
    ], string='Status')

    disapproval_reason = fields.Char(string="Reason for Disapproval")
    show_request = fields.Char()
    approval_type_id = fields.Many2one('purchase.approval.types')
    approval_id = fields.Many2one('purchase.approval')
    is_approver = fields.Boolean(compute="_compute_approver")
    approval_link = fields.Char('Approval link')

    current_date = fields.Date(default=fields.Datetime.now())
    # formatted_date = datetime.strftime(current_date, "%d-%B-%Y")

    check_status = fields.Char(compute='compute_check_status', store=True)

    @api.depends('approval_status', 'state')
    def compute_check_status(self):
        for rec in self:
            if rec.approval_status == 'disapprove' or rec.state == 'disapprove':
                print('Disapprove')
                self.submit_for_disapproval()
                # return send_email
            elif rec.approval_status == 'pr_approval' or rec.state == 'to_approve':
                print('To Approve')

    def test(self):
        for line in self.line_ids:
            print(line.id)
            print(line.schedule_date)
    def update_check_status(self):
        self.check_status = False
        self.check_status = True

    # @api.onchange('approval_status')
    # def _onchange_approval_status(self):
    #     if self.approval_status == 'disapprove':
    #         template_id = self.env.ref(
    #             'module_name.template_id')  # Replace 'module_name' with the actual name of your module, and 'template_id' with the ID or XML ID of the email template created in step 2
    #         template_id.send_mail(self.id, force_send=True)

    def approval_dashboard_link(self):
        action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.requisition')], limit=1)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        result_1 = re.sub(r'\((.*?)\)', '', str(action)).replace(',', '')
        res = f"{result_1},{action.id}"
        result = re.sub(r'\s*,\s*', ',', res)

        menu = self.env['ir.ui.menu'].search([('action', '=', result)], limit=1)
        params = {
            "action": 1197,
            "model": "purchase.requisition",
            "view_type": "list",
            "cids": "",
            "menu_id": menu.id
        }

        query_string = '&'.join([f'{key}={value}' for key, value in params.items()])
        list_view_url = f"{base_url}/web?debug=1#{query_string}"

        print(list_view_url)
        return list_view_url

    def generate_odoo_link(self):
        action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.requisition')], limit=1)
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        result = re.sub(r'\((.*?)\)', '', str(action)).replace(',', '')
        res = f"{result},{action.id}"
        result = re.sub(r'\s*,\s*', ',', res)

        menu = self.env['ir.ui.menu'].search([('action', '=', result)], limit=1)
        params = {
            "id": self.id,
            "action": action.id,
            "model": "purchase.requisition",
            "view_type": "form",
            "cids": 1,
            "menu_id": menu.id
        }
        query_params = "&".join(f"{key}={value}" for key, value in params.items())
        pr_form_link = f"{base_url}/web#{query_params}"
        return pr_form_link

    def action_in_progress(self):
        self.ensure_one()
        if not all(obj.line_ids for obj in self):
            raise UserError(_("You cannot confirm agreement {} because there is no product line.").format(self.name))
        if self.type_id.quantity_copy == 'none' and self.vendor_id:
            for requisition_line in self.line_ids:
                if requisition_line.price_unit <= 0.0:
                    raise UserError(_('You cannot confirm the blanket order without price.'))
                if requisition_line.product_qty <= 0.0:
                    raise UserError(_('You cannot confirm the blanket order without quantity.'))
                requisition_line.create_supplier_info()
            self.write({'state': 'to_approve'})
        else:
            self.write({'state': 'to_approve'})
        # Set the sequence number regarding the requisition type
        if self.name == 'New':
            if self.is_quantity_copy != 'none':
                self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.purchase.tender')
            else:
                self.name = self.env['ir.sequence'].next_by_code('purchase.requisition.blanket.order')

        self.write({
            'show_submit_request': True
        })

    def _compute_approver(self):
        for rec in self:
            if self.env.user == rec.approver_id.user_id:
                self.update({
                    'is_approver': True,

                })
            else:
                self.update({
                    'is_approver': False,
                })

    def generate_token(self):
        now = datetime.datetime.now()
        token = "{}-{}-{}-{}".format(self.id, self.name, self.env.user.id, now)
        return hashlib.sha256(token.encode()).hexdigest()

    def submit_for_approval(self):
        # Approval Dashboard Link Section
        approval_action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.requisition')],
                                                                   limit=1)
        approval_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        approval_result_1 = re.sub(r'\((.*?)\)', '', str(approval_action)).replace(',', '')
        approval_res = f"{approval_result_1},{approval_action.id}"
        approval_result = re.sub(r'\s*,\s*', ',', approval_res)

        approval_menu = self.env['ir.ui.menu'].search([('action', '=', approval_result)], limit=1)
        approval_params = {
            "action": 1197,
            "model": "purchase.requisition",
            "view_type": "list",
            "cids": "",
            "menu_id": approval_menu.id
        }

        approval_query_string = '&'.join([f'{key}={value}' for key, value in approval_params.items()])
        approval_list_view_url = f"{approval_base_url}/web?debug=1#{approval_query_string}"

        # Generate Odoo Link Section
        odoo_action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.requisition')], limit=1)
        odoo_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        odoo_result = re.sub(r'\((.*?)\)', '', str(odoo_action)).replace(',', '')
        odoo_res = f"{odoo_result},{odoo_action.id}"
        odoo_result = re.sub(r'\s*,\s*', ',', odoo_res)

        odoo_menu = self.env['ir.ui.menu'].search([('action', '=', odoo_result)], limit=1)
        odoo_params = {
            "id": self.id,
            "action": odoo_action.id,
            "model": "purchase.requisition",
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

        for rec in self:
            self.write({
                'approval_status': 'pr_approval',
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
        msg['Subject'] = 'Odoo Purchasing Mailer - Purchase Request For Approval [' + self.name + ']'

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
                <dd>Requested by: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
                <dd>Date Requested: &nbsp;&nbsp;{self.ordering_date if self.ordering_date != False else ""}</dd>
                <dd>Vendor: &nbsp;&nbsp;{self.vendor_id.name if self.vendor_id.name != False else ""}</dd>
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
                        <th>Quantity</th>
                        <th>Ordered Quantities</th>
                        <th>UoM</th>
                        <th>Scheduled Date</th>
                        <th>Unit Price</th>
                        <th>Subtotal</th>
                    </tr>
                    """

        for line in self.line_ids:
            html_content += f"""
                    <tr>
                        <td>{line.product_id.name}</td>
                        <td>{line.product_qty}</td>
                        <td>{line.qty_ordered}</td>
                        <td>{line.product_uom_id.name}</td>
                        <td>{line.schedule_date if line.schedule_date != False else ""}</td>
                        <td>{line.price_unit}</td>
                        <td>{line.subtotal}</td>
                    </tr>
        """

        html_content += f"""
            </table>
            <br></br>
                <span><b>JUSTIFICATION</b></span>
                <dd>{self.justification if self.justification != False else ""}</dd>
            </body>
            <br></br>
            <br></br>
            <br></br>
            <span style="font-style: italic;";><a href="{approval_url}"  style="color: green;">APPROVE</a> / <a href="{disapproval_url}"  style="color: red;">DISAPPROVE</a> / <a href="{pr_form_link}"  style="color: blue;">ODOO PR FORM
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

    def submit_for_disapproval(self):
        # Generate Odoo Link Section
        odoo_action = self.env['ir.actions.act_window'].search([('res_model', '=', 'purchase.requisition')], limit=1)
        odoo_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        odoo_result = re.sub(r'\((.*?)\)', '', str(odoo_action)).replace(',', '')
        odoo_res = f"{odoo_result},{odoo_action.id}"
        odoo_result = re.sub(r'\s*,\s*', ',', odoo_res)

        odoo_menu = self.env['ir.ui.menu'].search([('action', '=', odoo_result)], limit=1)
        odoo_params = {
            "id": self.id,
            "action": odoo_action.id,
            "model": "purchase.requisition",
            "view_type": "form",
            "cids": 1,
            "menu_id": odoo_menu.id
        }
        odoo_query_params = "&".join(f"{key}={value}" for key, value in odoo_params.items())
        pr_form_link = f"{odoo_base_url}/web#{odoo_query_params}"

        self.generate_odoo_link()

        fetch_getEmailReceiver = 'alex.mercado@teamglac.com'  # self.approver_id.work_email DEFAULT RECEIVER CHANGE IT TO IF YOU WANT ----> IF YOU WANT TO SET AS DEFAULT OR ONLY ONE ##
        self.send_disapproval_email(fetch_getEmailReceiver, pr_form_link)

        # for rec in self:
        #     self.write({
        #         'approval_status': 'pr_approval',
        #         'to_approve': True,
        #         'show_submit_request': False
        #     })

    def send_disapproval_email(self, fetch_getEmailReceiver, pr_form_link):
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
        msg['Subject'] = 'Odoo Purchasing Mailer - Purchase Request Disapproved [' + self.name + ']'

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
                <dd>Requested by: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
                <dd>Date Requested: &nbsp;&nbsp;{self.ordering_date if self.ordering_date != False else ""}</dd>
                <dd>Disapproved by: &nbsp;&nbsp;{self.user_id.name if self.user_id.name != False else ""}</dd>
                <dd>Disapproval date: &nbsp;&nbsp;{self.current_date if self.current_date != False else ""}</dd>
                <dd>Reason for Disapproval: &nbsp;&nbsp;{self.disapproval_reason if self.disapproval_reason != False else ""}</dd>
            <br></br>
            <br></br>
                <dd>Vendor: &nbsp;&nbsp;{self.vendor_id.name if self.vendor_id.name != False else ""}</dd> 
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
                        <th>Quantity</th>
                        <th>Ordered Quantities</th>
                        <th>UoM</th>
                        <th>Scheduled Date</th>
                        <th>Unit Price</th>
                        <th>Subtotal</th>
                    </tr>
                    """

        for line in self.line_ids:
            html_content += f"""
                    <tr>
                        <td>{line.product_id.name}</td>
                        <td>{line.product_qty}</td>
                        <td>{line.qty_ordered}</td>
                        <td>{line.product_uom_id.name}</td>
                        <td>{line.schedule_date if line.schedule_date != False else ""}</td>
                        <td>{line.price_unit}</td>
                        <td>{line.subtotal}</td>
                    </tr>
        """

        html_content += f"""
            </table>
            <br></br>
                <span><b>JUSTIFICATION</b></span>
                <dd>{self.justification if self.justification != False else ""}</dd>
            </body>
            <br></br>
            <br></br>
            <br></br>
            <span> <a href="{pr_form_link}" style="color: blue;">ODOO PR FORM</span>

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

    @api.onchange('department_id', 'approval_stage')
    def get_approver_domain(self):
        for rec in self:
            domain = []
            res = self.env["department.approvers"].search(
                [("dept_name", "=", rec.department_id.id), ("approval_type.name", '=', 'Purchase Requests')])

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

    @api.depends('approval_stage')
    def approve_request(self):
        for rec in self:
            res = self.env["department.approvers"].search(
                [("dept_name", "=", rec.department_id.id), ("approval_type.name", '=', 'Purchase Requests')])
            if rec.approver_id and rec.approval_stage < res.no_of_approvers:
                if rec.approval_stage == 1:
                    approver_dept = [x.second_approver.id for x in res.set_second_approvers]
                    self.write({
                        'approver_id': approver_dept[0]
                    })

                if rec.approval_stage == 2:
                    approver_dept = [x.third_approver.id for x in res.set_third_approvers]
                    self.write({
                        'approver_id': approver_dept[0]
                    })
                if rec.approval_stage == 3:
                    approver_dept = [x.fourth_approver.id for x in res.set_fourth_approvers]
                    self.write({
                        'approver_id': approver_dept[0]
                    })
                if rec.approval_stage == 4:
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

    def button_cancel(self):
        for order in self:
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(
                        _("Unable to cancel this purchase order. You must first cancel the related vendor bills."))

        self.write({'state': 'cancel',
                    'approval_status': 'cancel'})
