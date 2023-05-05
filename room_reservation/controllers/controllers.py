# -*- coding: utf-8 -*-
# from odoo import http


# class RoomReservation(http.Controller):
#     @http.route('/room_reservation/room_reservation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/room_reservation/room_reservation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('room_reservation.listing', {
#             'root': '/room_reservation/room_reservation',
#             'objects': http.request.env['room_reservation.room_reservation'].search([]),
#         })

#     @http.route('/room_reservation/room_reservation/objects/<model("room_reservation.room_reservation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('room_reservation.object', {
#             'object': obj
#         })
