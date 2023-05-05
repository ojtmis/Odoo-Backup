# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Room(models.Model):
    _name = 'reservation.room'
    _description = 'Room Reservation'

    name = fields.Char(string='Room Name', required=True, help='Name of the Room')
    room_no = fields.Integer(string='Room No.')
    location = fields.Text()
    description = fields.Text()

    responsible_id = fields.Many2one('res.users', string='Responsible', ondelete='set null', index=True)

    session_ids = fields.One2many('reservation.session', 'room_id', string='Sessions')


class Session(models.Model):
    _name = 'reservation.session'
    _description = 'Room Sessions'

    name = fields.Char(required=True)

    start_date = fields.Datetime(default=fields.Datetime.now())
    end_date = fields.Datetime(default=fields.Datetime.now())

    seats = fields.Integer(string='Number of seats')
    active = fields.Boolean(default=True)

    reserver_id = fields.Many2one('res.partner', string='Reserver')
    room_id = fields.Many2one('reservation.room', string='Room', ondelete='cascade', required=True, default=2)

    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    taken_seats = fields.Float(string='Taken seats', compute='_taken_seats')

    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)
    color = fields.Integer()

    @api.onchange('room_id', 'start_date', 'end_date')
    def _validate_sessions(self):
        room = self.room_id.id
        start = self.start_date
        end = self.end_date

        qry = """SELECT room_id, start_date, end_date  FROM public.reservation_session
                WHERE room_id = {0} AND start_date
                BETWEEN  '{1}' AND '{2}'""".format(room, start, end)
        print(qry)
        self.env.cr.execute(qry)
        res = self.env.cr.dictfetchone()
        print(res)

        if res is None:
            return None
        else:
            # raise ValidationError("Sorry room is already occupied at that date or time!\nPlease! insert a new date or time")
            return {
                'warning': {
                    'title': "Room Occupied",
                    'message': "Sorry room is already occupied at that date or time!\nPlease! insert a new date or time"
                },
            }

    @api.onchange('start_date', 'end_date')
    def _validate_start_date(self):
        if self.start_date > self.end_date:
            raise ValidationError("Date or Time entered is in the past!")

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative"
                },
            }
    #     if self.seats < len(self.attendee_ids):
    #         return {
    #             'warning': {
    #                 'title': "Too many attendees",
    #                 'message': "Increase seats or remove excess attendees",
    #             },
    #         }
