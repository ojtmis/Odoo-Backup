# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    department_id = fields.Many2one('account.analytic.account', string="Department", store=True)
    approver_id = fields.Many2one('hr.employee', string="First Approver",
                                  domain=lambda self: self.get_approver_domains())
    job_title_4 = fields.Char('hr.employee', related="approver_id.job_title")

    second_approver_id = fields.Many2one('hr.employee', string="Second Approver",
                                         domain=lambda self: self.get_approver_domains())
    job_title_2 = fields.Char('hr.employee', related="second_approver_id.job_title")

    third_approver_id = fields.Many2one('hr.employee', string="Third Approver",
                                        domain=lambda self: self.get_approver_domains())
    job_title_3 = fields.Char('hr.employee', related="third_approver_id.job_title")

    fourth_approver_id = fields.Many2one('hr.employee', string="Fourth Approver",
                                         domain=lambda self: self.get_approver_domains())
    job_title_1 = fields.Char('hr.employee', related="fourth_approver_id.job_title")

    fifth_approver_id = fields.Many2one('hr.employee', string="Fifth Approver",
                                        domain=lambda self: self.get_approver_domains())
    job_title_5 = fields.Char('hr.employee', related="fifth_approver_id.job_title")

    approver_count = fields.Integer(string='Count')

    # this checks that no two fields contain the same approver name.
    # @api.onchange('approver_id', 'second_approver_id', 'third_approver_id', 'fourth_approver_id', 'fifth_approver_id')
    # def _check_approver_uniqueness(self):
    #     for rec in self:
    #         approvers = [rec.approver_id.name, rec.second_approver_id.name, rec.third_approver_id.name, rec.fourth_approver_id.name, rec.fifth_approver_id.name]
    #
    #         for i, approver in enumerate(approvers):
    #             # check if the current approver name is not empty and if it is already present in the list of approvers before it.
    #             if approver and approver in approvers[:i]:
    #                 raise ValidationError(f"{approver} is already selected as an approver.")

    @api.onchange('department_id')
    def no_ofapprovers(self):
        department_approvers = self.env['department.approvers'].search([('dept_name', '=', self.department_id.id)])
        count = 0.
        for approver in department_approvers:
            count += approver.no_of_approvers
        self.approver_count = count
        print('approver count: ', self.approver_count)

    # @api.depends('approval_stage', 'approver_stage')
    # def approve_request(self):
    #     for rec in self:
    #         res = self.env["department.approvers"].search(
    #             [("dept_name", "=", rec.department_id.id), ("approval_type.name", '=', 'Purchase Requests')])
    #
    #         print('approve request function')
    #
    #         if rec.approver_id and rec.approval_stage < res.no_of_approvers:
    #             print('Approver name: ', rec.approver_id.name, '| stage: ', rec.approval_stage, '| total approvers: ',  res.no_of_approvers)
    #             if rec.approver_stage == 'pending_approval_1':
    #                 # approver_dept = [x.first_approver.id for x in res.set_first_approvers]
    #                 print(self.approver_stage)
    #                 self.write({
    #                     # 'approver_id': approver_dept[0],
    #                     'approver_stage': 'pending_approval_2',
    #                     'state': 'to_approve',
    #                     'approval_status': 'pr_approval'
    #                 })
    #
    #         # if rec.second_approver_id and rec.approval_stage < res.no_of_approvers:
    #
    #             if rec.approval_stage == 2:
    #                 print('Second Approver')
    #                 print('is_approver', self.is_approver)
    #                 approver_dept = [x.second_approver.id for x in res.set_second_approvers]
    #                 print('stage 2 :', approver_dept)
    #                 print(self.approver_stage)
    #                 self.write({
    #                     # 'second_approver_id': approver_dept[0],
    #                     'approver_stage': 'pending_approval_3',
    #                     'state': 'to_approve',
    #                     'approval_status': 'pr_approval'
    #                 })
    #
    #             if rec.approval_stage == 3:
    #                 approver_dept = [x.third_approver.id for x in res.set_third_approvers]
    #                 print('stage 3 :', approver_dept)
    #                 self.write({
    #                     'third_approver_id': approver_dept[0]
    #                 })
    #             if rec.approval_stage == 4:
    #                 approver_dept = [x.fourth_approver.id for x in res.set_fourth_approvers]
    #                 print('stage 4 :', approver_dept)
    #
    #                 self.write({
    #                     'fourth_approver_id': approver_dept[0]
    #                 })
    #             if rec.approval_stage == 5:
    #                 approver_dept = [x.fifth_approver.id for x in res.set_fifth_approvers]
    #                 print('stage 5 :', approver_dept)
    #                 self.write({
    #                     'fifth_approver_id': approver_dept[0]
    #                 })
    #             rec.approval_stage += 1
    #             print('last stage= ', rec.approval_stage)
    #         else:
    #             print("state: to_approve, "
    #                   "approval_status: pr_approval")
    #
    #             # self.write({
    #             #     'state': 'approved',
    #             #     'approval_status': 'approved'
    #             # })

    # @api.depends('approval_stage')
    # def approve_request(self):
    #     for rec in self:
    #         res = self.env["department.approvers"].search(
    #             [("dept_name", "=", rec.department_id.id), ("approval_type.name", '=', 'Purchase Requests')])
    #         if rec.approver_id and rec.approval_stage < res.no_of_approvers:
    #             if rec.approval_stage == 1:
    #                 approver_dept = [x.second_approver.id for x in res.set_second_approvers]
    #                 self.write({
    #                     'approver_id': approver_dept[0]
    #                 })
    #
    #             if rec.approval_stage == 2:
    #                 approver_dept = [x.third_approver.id for x in res.set_third_approvers]
    #                 self.write({
    #                     'approver_id': approver_dept[0]
    #                 })
    #             if rec.approval_stage == 3:
    #                 approver_dept = [x.fourth_approver.id for x in res.set_fourth_approvers]
    #                 self.write({
    #                     'approver_id': approver_dept[0]
    #                 })
    #             if rec.approval_stage == 4:
    #                 approver_dept = [x.fifth_approver.id for x in res.set_fifth_approvers]
    #                 self.write({
    #                     'approver_id': approver_dept[0]
    #                 })
    #             rec.approval_stage += 1
    #         else:
    #             self.write({
    #                 'state': 'approved',
    #                 'approval_status': 'approved'
    #             })

    # def test(self):
    #     for rec in self:
    #         if rec.department_id and rec.approval_stage == 1:
    #             res = self.env["department.approvers"].search([
    #                 ("dept_name", "=", rec.department_id.id),
    #                 ("approval_type.name", "=", 'Purchase Requests')
    #             ])


    @api.onchange('department_id', 'approval_stage')
    def get_approver_domains(self):
        domain = []
        for rec in self:
            if rec.department_id and rec.approval_stage == 1:
                res = self.env["department.approvers"].search([
                    ("dept_name", "=", rec.department_id.id),
                    ("approval_type.name", "=", 'Purchase Requests')
                ])

                if res:
                    approver_dept = [x.first_approver.id for x in res.set_first_approvers]
                    rec.approver_id = approver_dept[0]
                    domain.append(('id', '=', approver_dept))

                    if len(res.set_second_approvers) > 0:
                        approver_dept = [x.second_approver.id for x in res.set_second_approvers]
                        rec.second_approver_id = approver_dept[0]
                        domain.append(('id', '=', approver_dept))

                    if len(res.set_third_approvers) > 0:
                        approver_dept = [x.third_approver.id for x in res.set_third_approvers]
                        rec.third_approver_id = approver_dept[0]
                        domain.append(('id', '=', approver_dept))
                        print('triggered 3')

                    if len(res.set_fourth_approvers) > 0:
                        approver_dept = [x.fourth_approver.id for x in res.set_fourth_approvers]
                        rec.fourth_approver_id = approver_dept[0]
                        domain.append(('id', '=', approver_dept))

                    if len(res.set_fifth_approvers) > 0:
                        approver_dept = [x.fifth_approver.id for x in res.set_fifth_approvers]
                        rec.fifth_approver_id = approver_dept[0]
                        domain.append(('id', '=', approver_dept))

        return {'domain': {
            'approver_id': domain,
            'second_approver_id': domain,
            'third_approver_id': domain,
            'fourth_approver_id': domain,
            'fifth_approver_id': domain,
        }}
