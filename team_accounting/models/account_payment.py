import math
import re

from num2words import num2words

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from collections import defaultdict

class account_payment(models.Model):
    _inherit = 'account.payment'
    _description = 'Account Payment Custom Inherit'

    word_num = fields.Float(string="Amount In Words", compute='remove_comma')
    word_move = fields.Char(string='Amount in Words', readonly=True)
    remove_monetary = fields.Float(compute='_remove_monetary')
    to_php = fields.Float('Php Value')
    add_data = fields.Float(compute='compute_add_data')

    get_currency_sign = fields.Float(compute='get_currency')

    move_currency = fields.Char()

    def get_currency(self):
        self.get_currency_sign = 0
        counter = 0
        for rec in self:
            counter = rec.currency_id.symbol == 'Php'
        self.move_currency = counter

    @api.depends('amount')
    def _remove_monetary(self):
        self.remove_monetary = 0
        for rec in self:
            rec.remove_monetary = rec.amount + 0
            rec.amount = rec.remove_monetary

    def compute_add_data(self):
        self.add_data = 0

        get_currency_name = self.currency_id.name
        #Checking if Currency Name is True

        if get_currency_name:
            if get_currency_name == 'PHP':
                currency = self.env['res.currency'].search([('name', '=', 'USD')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                print(save_record)
                debit_here = 0
                # get currency from amount end
                compute_here = self.amount
                self.to_php = compute_here
                print(compute_here)
            elif get_currency_name == 'USD':
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                print(save_record)
                # get currency from amount end
                compute_here = self.amount * save_record
                self.to_php = compute_here
                print(compute_here)
            elif get_currency_name == 'EUR':
                currency = self.env['res.currency'].search([('name', '=', 'EUR')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = list(data_here.values())
                save_record = 0
                for rec in number:
                    save_record = int(rec)
                print(save_record)
                # get currency from amount end
                compute_here = self.amount * save_record
                self.to_php = compute_here
                print(compute_here)
            elif get_currency_name == 'JPY':
                print('JPY')
            else:
                print('Error')
        else:
            print('Error')

    def print_check_voucher(self):
        print_here = self.env.ref('team_accounting.action_report_check_voucher').report_action(self)
        return print_here

    def print_payable_voucher_partial(self):
        print_here = self.env.ref('team_accounting.action_report_payment_voucher_partial').report_action(self)
        return print_here

    def print_payable_voucher_whole(self):
        print_here = self.env.ref('team_accounting.action_report_payment_voucher').report_action(self)
        return print_here

    def remove_comma(self):
        self.word_num = 0
        for x in self:
            print(x)
            dollars, cents = str(x.to_php).split(".")
            # Convert the dollar amount to words
            dollar_words = num2words(dollars)
            print(dollar_words)

            # If the amount has no cents, return the dollar amount with "Only"
            if cents == "00":
                print("{} only".format(dollar_words))
                word = "{} only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str)
                self.word_move = test_str
            # If the amount has cents, convert the cents to a fraction and combine with the dollar amount
            elif cents == "0":
                print("{} only".format(dollar_words))
                word = "{} only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str)
                self.word_move = test_str
            else:
                print('Go in Else')
                cents_int = cents
                cent_int = list(map(int, str(cents_int)))
                print(cent_int)
                counting_cents_stored = len(cent_int)
                if counting_cents_stored == 1:
                    print(counting_cents_stored)
                    cent_fraction = "{}0/100".format(cents)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str)
                    self.word_move = test_str
                else:
                    print(counting_cents_stored)
                    cent_fraction = "{}/100".format(cents)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str)
                    self.word_move = test_str
                ##END



