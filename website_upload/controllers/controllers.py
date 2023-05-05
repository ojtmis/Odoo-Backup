# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteUpload(http.Controller):
#     @http.route('/website_upload/website_upload/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_upload/website_upload/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_upload.listing', {
#             'root': '/website_upload/website_upload',
#             'objects': http.request.env['website_upload.website_upload'].search([]),
#         })

#     @http.route('/website_upload/website_upload/objects/<model("website_upload.website_upload"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_upload.object', {
#             'object': obj
#         })
