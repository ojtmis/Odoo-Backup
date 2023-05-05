# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    # first_department_id = fields.Many2one('account.analytic.account', string="Department", store=True)
    first_approver_id = fields.Many2one('hr.employee', string="[1] Approver",
                                        domain=lambda self: self.get_approver_domain())
    job_title_1 = fields.Char('hr.employee', related="first_approver_id.job_title")

    second_approver_id = fields.Many2one('hr.employee', string="[2] Approver",
                                         domain=lambda self: self.get_approver_domain())
    job_title_2 = fields.Char('hr.employee', related="second_approver_id.job_title")

    third_approver_id = fields.Many2one('hr.employee', string="[3] Approver",
                                        domain=lambda self: self.get_approver_domain())
    job_title_3 = fields.Char('hr.employee', related="third_approver_id.job_title")

    approver_id = fields.Many2one('hr.employee', string="Initial Approver", domain=lambda self: self.get_approver_domain())
    job_title_4 = fields.Char('hr.employee', related="approver_id.job_title")

    # this checks that no two fields contain the same approver name.
    @api.onchange('first_approver_id', 'second_approver_id', 'third_approver_id')
    def _check_approver_uniqueness(self):
        for record in self:
            approvers = [record.first_approver_id.name, record.second_approver_id.name, record.third_approver_id.name]

            for i, approver in enumerate(approvers):
                # check if the current approver name is not empty and if it is already present in the list of approvers before it.
                if approver and approver in approvers[:i]:
                    raise ValidationError(f"{approver} is already selected as an approver.")

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


    # @api.onchange('first_department_id', 'approval_stage')
    # def get_approver_domain_1(self):
    #         for rec in self:
    #             domain = []
    #             res = self.env["department.approvers"].search(
    #                 [("dept_name", "=", rec.first_department_id.id), ("approval_type.name", '=', 'Purchase Requests')])
    #
    #             if rec.first_department_id and rec.approval_stage == 1:
    #                 try:
    #                     approver_dept = [x.first_approver.id for x in res.set_first_approvers]
    #                     rec.first_approver_id = approver_dept[0]
    #                     domain.append(('id', '=', approver_dept))
    #
    #                 except IndexError:
    #                     raise UserError(_("No Approvers set for {}!").format(rec.first_department_id.name))
    #             else:
    #                 domain = []
    #
    #             return {'domain': {'first_approver_id': domain}}