# -*- coding: utf-8 -*-
# from odoo import http


# class ApprovalModuleExtension(http.Controller):
#     @http.route('/approval_module_extension/approval_module_extension/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/approval_module_extension/approval_module_extension/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('approval_module_extension.listing', {
#             'root': '/approval_module_extension/approval_module_extension',
#             'objects': http.request.env['approval_module_extension.approval_module_extension'].search([]),
#         })

#     @http.route('/approval_module_extension/approval_module_extension/objects/<model("approval_module_extension.approval_module_extension"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('approval_module_extension.object', {
#             'object': obj
#         })
