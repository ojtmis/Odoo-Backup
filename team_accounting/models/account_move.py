import re

from num2words import num2words

from odoo import models, fields, api


# Employee Name: John Raymark Llavanes
# Employee ID: 10450

# """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....

class account_move(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move Custom Inherit'

    forex_exchange = fields.Float(string='Forex Exchange')
    percentage = fields.Float(string='Percentage Added')
    amount_total_in_php = fields.Float(string='Total Amount in PHP')
    divided_usd = fields.Float(string='Divided USD', digits=(12, 3))
    total_usd = fields.Float(string='Total US$')
    compute_total_usd = fields.Float(string='Total US$', compute='_compute_total_usd')
    computed_total = fields.Float(string='Processing Fee', compute='_compute_total')
    percentage_get_total = fields.Float(compute="_compute_percentage_get_total")
    total_amount_without_monetary = fields.Float('Total Amount')
    remove_monetary = fields.Float(compute='_remove_monetary')
    total_amount_without_monetary1 = fields.Float('Total Amount')
    word_num = fields.Char(string="Amount In Words:", compute='remove_comma', readonly=True)
    word_move = fields.Char(string='Amount in Words', readonly=True)
    word_move2 = fields.Char(string='Amount in Words', readonly=True)
    get_currency_name = fields.Float(compute="get_name_currency")
    currency_name_here = fields.Char('Currency Name')
    word_num2 = fields.Char(string="Amount In Words:", compute='remove_comma2', readonly=True)
    word_move2 = fields.Char(string='Amount in Words', readonly=True)

    word_for_journal_entries = fields.Char(string='Amount in Words', compute='word_journal', readonly=True)
    word_for_journal_entries_val = fields.Char(string='Amount in Words')

    get_total_in_deb_cred_compute = fields.Float(compute='calculate_journal')
    get_total_in_deb_cred = fields.Float('Journal Items Total Amount')

    debit_here = fields.Float(compute='get_journal')

    debit_payable = fields.Float(compute='get_journal_payable')

    add_percent = fields.Float()

    saving_forex_php_value = fields.Float()
    saving_forex_php_value_ap = fields.Float()

    adding_usd_with_percent_value = fields.Float()

    computing_forex_and_amm = fields.Float(compute='computing_forex_and_amm_var')
    forex_and_amm_val = fields.Float()

    getting_total_of_debit_credit_var = fields.Float(compute='getting_total_of_debit_credit')
    getting_total_of_debit_credit_val = fields.Float()

    total_credit_val = fields.Float()

    deduct_value = fields.Float()

    amm_total_usd = fields.Float()

    fetch_recheck_compute = fields.Float(compute='recheck_calculate')
    fetch_recheck_data = fields.Float()

    amm_usd_val = fields.Float()

    get_query_here_ap = fields.Float(compute='_getting_query_ap')
    get_query_here = fields.Float(compute='_getting_query')
    set_query_here = fields.Float()

    @api.depends('getting_total_of_debit_credit_val')
    def recheck_calculate(self):
        self.fetch_recheck_compute = 0
        fetch_and_recalculate_minus = self.getting_total_of_debit_credit_val * 0.05
        fetch_and_recalculate_total_retotal = round(
            self.getting_total_of_debit_credit_val - fetch_and_recalculate_minus, 2)
        self.fetch_recheck_data = fetch_and_recalculate_total_retotal

    @api.depends('line_ids')
    def getting_total_of_debit_credit(self):
        self.getting_total_of_debit_credit_var = 0
        a = 0
        for rec in self.line_ids:
            a += rec.credit
        self.getting_total_of_debit_credit_val = round(a,
                                                       2)  # <-- Remove this and uncomment the code below to activate more than 2 Floating Point... """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....

    # For this function this is for debit credit and the fields / data require for that report .. """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....

    @api.depends('currency_id', 'getting_total_of_debit_credit_val', 'forex_and_amm_val')
    def computing_forex_and_amm_var(self):
        self.computing_forex_and_amm = 0
        get_currency_payable = self.currency_id
        get_curr_name = 0
        for rec in get_currency_payable:
            get_curr_name = rec.name
        if get_curr_name:
            if get_curr_name == 'PHP':

                calc = self.forex_and_amm_val = self.getting_total_of_debit_credit_val
                amm_usd = calc / self._getting_query_ap()
                self.amm_usd_val = amm_usd
                minus = self.amm_usd_val * 0.05
                self.add_percent = minus
                total_with_percent = amm_usd - minus
                self.deduct_value = round(total_with_percent, 2)
                total = total_with_percent + self.add_percent
                self.adding_usd_with_percent_value = round(total,
                                                           2)  # <-- Remove this and uncomment the code below to activate more than 2 Floating Point... """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....

            elif get_curr_name == 'USD':

                calc = self.forex_and_amm_val = self.getting_total_of_debit_credit_val
                amm_usd = calc / self._getting_query_ap()
                self.amm_usd_val = amm_usd
                minus = self.amm_usd_val * 0.05
                self.add_percent = minus
                total_with_percent = amm_usd - minus
                self.deduct_value = round(total_with_percent, 2)
                total = total_with_percent + self.add_percent
                self.adding_usd_with_percent_value = round(total,
                                                           2)  # <-- Remove this and uncomment the code below to activate more than 2 Floating Point... """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....

            elif get_curr_name == 'EUR':

                calc = self.forex_and_amm_val = self.getting_total_of_debit_credit_val
                amm_usd = calc / self._getting_query_ap()
                self.amm_usd_val = amm_usd
                minus = self.amm_usd_val * 0.05
                self.add_percent = minus
                total_with_percent = amm_usd - minus
                self.deduct_value = round(total_with_percent, 2)
                total = total_with_percent + self.add_percent
                self.adding_usd_with_percent_value = total

            # In Here if you want to add more currency just view on Currencies > CURRENCY NAME and add CUR ABBREVIATION #
            else:
                print('Error')
        else:
            print('Error')

    # In Here This function is just for AP VOUCHER this function is base on DATE, it fetch date and compare to currencies date
    @api.depends('date')
    def _getting_query_ap(self):
        self.get_query_here_ap = 0
        currency = self.env['res.currency'].search([('name', '=', 'PHP')])
        currency_id_here = currency.id
        set_date = ''
        for get_date in self:
            set_date = get_date.date
        fetched_date = set_date
        if not fetched_date:
            currency = self.env['res.currency'].search([('name', '=', 'PHP')])
            currency_id_here = currency.id
            query = "SELECT rate FROM public.res_currency_rate where currency_id = %s ORDER BY name DESC" % currency_id_here
            self.env.cr.execute(query)
            data_here = self.env.cr.dictfetchone()
            print(data_here)
            number = data_here.values()
            save_record = 0
            for rec in number:
                save_record = rec
            print(save_record, '<--- No Date AP')
            self.saving_forex_php_value_ap = save_record
            return save_record
        else:
            query = "SELECT rate FROM public.res_currency_rate WHERE name='%s'" % fetched_date
            self.env.cr.execute(query)
            data_here = self.env.cr.dictfetchone()
            print(data_here, 'Tesssssssssssssttttingggg')
            if data_here is None:
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s ORDER BY name DESC" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = data_here.values()
                save_record = 0
                for rec in number:
                    save_record = rec
                print(save_record, '<--- No Date AP')
                self.saving_forex_php_value_ap = save_record
                return save_record
            else:
                query = "SELECT rate FROM public.res_currency_rate WHERE (currency_id=%s AND name='%s')" % (
                    currency_id_here, fetched_date)
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                number = data_here.values()
                save_record = 0
                for rec in number:
                    save_record = rec
                print(save_record, '<--- With Date AP')
                self.saving_forex_php_value_ap = save_record
                return save_record

    # In Here This function is just for DEBIT CREDIT VOUCHER this function is base on INVOICE DATE, it fetch date and compare to currencies date
    @api.depends('invoice_date')
    def _getting_query(self):
        self.get_query_here = 0
        currency = self.env['res.currency'].search([('name', '=', 'PHP')])
        currency_id_here = currency.id
        set_date = ''
        for get_date in self:
            set_date = get_date.invoice_date
        fetched_date = set_date
        if not fetched_date:
            currency = self.env['res.currency'].search([('name', '=', 'PHP')])
            currency_id_here = currency.id
            query = "SELECT rate FROM public.res_currency_rate where currency_id = %s ORDER BY name DESC" % currency_id_here
            self.env.cr.execute(query)
            data_here = self.env.cr.dictfetchone()
            print(data_here)
            number = data_here.values()
            save_record = 0
            for rec in number:
                save_record = rec
            print(save_record, '<--- No Date')
            self.saving_forex_php_value = save_record
            return save_record
        else:
            query = "SELECT rate FROM public.res_currency_rate WHERE name='%s'" % fetched_date
            self.env.cr.execute(query)
            data_here = self.env.cr.dictfetchone()
            print(data_here, 'Tesssssssssssssttttingggg')
            if data_here is None:
                currency = self.env['res.currency'].search([('name', '=', 'PHP')])
                currency_id_here = currency.id
                query = "SELECT rate FROM public.res_currency_rate where currency_id = %s ORDER BY name DESC" % currency_id_here
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = data_here.values()
                save_record = 0
                for rec in number:
                    save_record = rec
                print(save_record, '<--- No Date')
                self.saving_forex_php_value = save_record
                return save_record
            else:
                query = "SELECT rate FROM public.res_currency_rate WHERE (currency_id=%s AND name='%s')" % (
                    currency_id_here, fetched_date)
                print(query, '<----- test')  # new (03-14-2023)
                self.env.cr.execute(query)
                data_here = self.env.cr.dictfetchone()
                print(data_here)
                number = data_here.values()
                save_record = 0
                for rec in number:
                    save_record = rec
                print(save_record, '<--- With Date')
                self.saving_forex_php_value = save_record
                return save_record

    # This function is for Payable Voucher or AP VOUCHER this function calculates debit and credit base on currency the """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT"""....
    # I call the function self._getting_query_ap() to calculate,. if you add field you getting error 

    @api.depends('currency_id', 'line_ids')
    def get_journal_payable(self):
        self.debit_payable = 0
        get_currency_payable = self.currency_id
        get_curr_name = 0
        for rec in get_currency_payable:
            get_curr_name = rec.name
        print(get_curr_name)
        if get_curr_name:
            if get_curr_name == 'PHP':
                # get currency USD

                # this is for debit
                for rec in self.line_ids:
                    get_debit = rec.debit
                    print(get_debit)
                    rec.debit_data_payable = get_debit
                    print(rec.debit_data_payable, '<----- Teeeesssttt Payable')

                # this is for credit
                for rec in self.line_ids:
                    get_credit = rec.credit
                    print(get_credit)
                    rec.credit_data_payable = get_credit
                    print(rec.credit_data_payable, '<----- Credit Payable')

            elif get_curr_name == 'USD':
                # get currency USD

                # this is for debit
                for rec in self.line_ids:
                    get_debit = rec.debit / self._getting_query_ap()
                    print(get_debit)
                    rec.debit_data_payable = get_debit
                    print(rec.debit_data_payable, '<----- Debit Payable')

                # this is for credit
                for rec in self.line_ids:
                    get_credit = rec.credit / self._getting_query_ap()
                    print(get_credit)
                    rec.credit_data_payable = get_credit
                    print(rec.credit_data_payable, '<----- Credit Payable')

            elif get_curr_name == 'EUR':
                # get currency EUR

                # this is for debit
                for rec in self.line_ids:
                    print(rec.credit, '<--- credit')
                    get_debit = rec.debit / self._getting_query_ap()
                    print(get_debit)
                    rec.debit_data_payable = get_debit
                    print(rec.debit_data_payable, '<----- Debit Payable')

                # this is for credit
                for rec in self.line_ids:
                    get_credit = rec.credit / self._getting_query_ap()
                    print(get_credit)
                    rec.credit_data_payable = get_credit
                    print(rec.credit_data_payable, '<----- Credit Payable')

            elif get_curr_name == 'JPY':
                print('JPY')
            else:
                print('Error')
        else:
            print('Error')

    # This function is for DEBIT CREDIT this function calculates debit and credit base on currency """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....
    # I call the function self._getting_query() to calculate,. if you add field you getting error 

    def get_journal(self):
        self.debit_here = 0
        currency = self.env['res.currency'].search([('name', '=', 'PHP')])
        get_rate = 0
        for rec in currency:
            get_rate = rec.rate
        for rec in self.line_ids:
            get_debit = rec.debit / self._getting_query()
            print(get_debit)
            rec.debit_data = get_debit
            print(rec.debit_data)
        for rec in self.line_ids:
            get_credit = rec.credit / self._getting_query()
            print(get_credit)
            rec.credit_data = get_credit
            print(rec.credit_data)

    # This Functions here is just for button

    def print_for_invoice_voucher(self):
        print_here = self.env.ref('team_accounting.account_vendor_bills_report').report_action(self)
        return print_here

    def print_for_payable_voucher(self):
        print_here = self.env.ref('team_accounting.ap_voucher_print_id').report_action(self)
        return print_here

    def print_for_credit_note_voucher(self):
        print_here = self.env.ref('team_accounting.debit_credit_report_id_here').report_action(self)
        return print_here

    def print_for_credit_note_voucher_v2(self):
        print_here = self.env.ref('team_accounting.debit_credit_report_id_wo_fee_here').report_action(self)
        return print_here

    def print_for_journal_entry_voucher(self):
        print_here = self.env.ref('team_accounting.action_report_payment_voucher_acc_move').report_action(self)
        return print_here

    # END FOR BUTTONS#

    def calculate_journal(self):
        self.get_total_in_deb_cred_compute = 0
        calculate_deb_cred = 0
        for rec in self.line_ids:
            calculate_deb_cred = calculate_deb_cred + rec.debit
        print(calculate_deb_cred)
        self.get_total_in_deb_cred = calculate_deb_cred

    @api.depends('currency_id')
    def get_name_currency(self):
        self.get_currency_name = 0
        name_here = ""
        for rec in self:
            name_here = rec.currency_id.name
            print(name_here)
        self.currency_name_here = name_here

    @api.depends('currency_id')
    def calculate_dropdown(self):
        currency_here = ""
        for rec in self:
            currency_here = rec.currency_id.rate_ids.rate
        print(currency_here, "<----- NEW")

    @api.depends('percentage', 'amount_total')
    def _compute_total(self):
        for rec in self:
            rec.computed_total = rec.amount_total * rec.percentage
            rec.divided_usd = rec.computed_total

    @api.depends('forex_exchange', 'amount_total')
    def _computed_php(self):
        for rec in self:
            rec.computed_php = rec.forex_exchange / rec.amount_total
            rec.amount_total_in_php = rec.computed_php

    @api.depends('percentage', 'amount_total')
    def _compute_percentage_get_total(self):
        for rec in self:
            rec.percentage_get_total = rec.percentage * rec.amount_total
            rec.divided_usd = rec.percentage_get_total

    @api.depends('amount_total', 'divided_usd')
    def _compute_total_usd(self):
        for rec in self:
            rec.compute_total_usd = rec.amount_total + rec.divided_usd
            rec.total_usd = rec.compute_total_usd

    @api.depends('amount_total')
    def _remove_monetary(self):
        for rec in self:
            rec.remove_monetary = rec.amount_total + 0
            rec.total_amount_without_monetary = rec.remove_monetary

    @api.depends('currency_id')
    def _compute_forex_ex(self):
        self.forex_ex = 0
        print('Compute Forex')
        get_currency_ex = self.currency_id.rate_ids
        for rec in get_currency_ex:
            exchange_rate = rec.rate
            self.forex_ex = exchange_rate
            record = self.write({
                'forex_exchange': exchange_rate,
            })
            return record

    # This Function is for Num2Words

    @api.depends('adding_usd_with_percent_value')
    def remove_comma(self):
        self.word_num = 0
        print('test1')
        for x in self:
            print(x)
            dollars, cents = str(x.adding_usd_with_percent_value).split(".")

            # Convert the dollar amount to words
            dollar_words = num2words(float(dollars))
            print(dollar_words)
            # If the amount has no cents, return the dollar amount with "Only"
            if cents == "00":
                print("{} Only".format(dollar_words))
                word = "{} Only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str.title())
                self.word_move = test_str.title()
            # If the amount has cents, convert the cents to a fraction and combine with the dollar amount 
            elif cents == "0":
                print("{} Only".format(dollar_words))
                word = "{} Only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str.title())
                self.word_move = test_str.title()
            else:
                print('Sample')
                cents_int = cents
                only_two_start_num = int(str(cents_int)[
                                         :2])  # <-- Remove this and uncomment the code below to activate more than 2 Floating Point... """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....
                # only_two_start_num = cents_int
                print(only_two_start_num, '<-- for Testing')
                cent_int = list(map(int, str(only_two_start_num)))
                print(cent_int, '<-- get size')
                counting_cents_stored = len(cent_int)
                print(type(counting_cents_stored), '<-- count length')
                if counting_cents_stored == 1:
                    print(counting_cents_stored)
                    only_two_start_num = int(str(cents)[:2])
                    # only_two_start_num = cents_int
                    print(only_two_start_num, '<---- test print hhere')
                    cent_fraction = "{}0/100".format(only_two_start_num)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str.title())
                    self.word_move = test_str.title()
                else:
                    print(counting_cents_stored)
                    only_two_start_num = int(str(cents)[
                                             :2])  # <-- Remove this and uncomment the code below to activate more than 2 Floating Point... """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....
                    # only_two_start_num = cents_int
                    print(only_two_start_num, '<---- test print double')
                    only_two_start_num = int(str(cents)[:2])
                    cent_fraction = "{}/100".format(only_two_start_num)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str.title())
                    self.word_move = test_str.title()
            print('end test1')

    @api.depends('amount_total_signed')
    def remove_comma2(self):
        self.word_num2 = 0
        print('sample')
        for x in self:
            print(x)
            dollars, cents = str(x.amount_total_signed).split(".")

            # Convert the dollar amount to words
            dollar_words = num2words(float(dollars))
            print(dollar_words)
            # If the amount has no cents, return the dollar amount with "Only"
            if cents == "00":
                print("{} Only".format(dollar_words))
                word = "{} Only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str.title())
                self.word_move2 = test_str.title()
            # If the amount has cents, convert the cents to a fraction and combine with the dollar amount
            elif cents == "0":
                print("{} Only".format(dollar_words))
                word = "{} Only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str.title())
                self.word_move2 = test_str.title()
            else:
                print('Sample')
                cents_int = cents
                only_two_start_num = int(str(cents_int)[:2])
                # only_two_start_num = cents_int
                print(only_two_start_num, '<-- for Testing')
                cent_int = list(map(int, str(only_two_start_num)))
                print(cent_int, '<-- get size')
                counting_cents_stored = len(cent_int)
                print(type(counting_cents_stored), '<-- count length')
                if counting_cents_stored == 1:
                    print(counting_cents_stored)
                    only_two_start_num = int(str(cents)[:2])
                    # only_two_start_num = cents_int
                    print(only_two_start_num, '<---- test print hhere')
                    cent_fraction = "{}0/100".format(only_two_start_num)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str.title())
                    self.word_move2 = test_str.title()
                else:
                    print(counting_cents_stored)
                    only_two_start_num = int(str(cents)[:2])
                    # only_two_start_num = cents_int
                    print(only_two_start_num, '<---- test print double')
                    only_two_start_num = int(str(cents)[:2])
                    cent_fraction = "{}/100".format(only_two_start_num)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str.title())
                    self.word_move2 = test_str.title()

    @api.depends('amount_total')
    def word_journal(self):
        self.word_for_journal_entries = 0
        print('test1')
        for x in self:
            print(x)
            dollars, cents = str(x.amount_total).split(".")

            # Convert the dollar amount to words
            dollar_words = num2words(float(dollars))
            print(dollar_words)
            # If the amount has no cents, return the dollar amount with "Only"
            if cents == "00":
                print("{} Only".format(dollar_words))
                word = "{} Only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str.title())
                self.word_for_journal_entries_val = test_str.title()
            # If the amount has cents, convert the cents to a fraction and combine with the dollar amount
            elif cents == "0":
                print("{} Only".format(dollar_words))
                word = "{} Only".format(dollar_words)
                remove_comma = re.sub(',', '', str(word))
                remove_dash = re.sub('-', ' ', str(remove_comma))
                word_in_arr = remove_dash.split(' ')
                print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                test_str = ''
                for rec_arr in word_in_arr:
                    if rec_arr != 'and':
                        test_str = test_str + rec_arr + ' '
                print(test_str.title())
                self.word_for_journal_entries_val = test_str.title()
            else:
                print('Sample')
                cents_int = cents
                only_two_start_num = int(str(cents_int)[
                                         :2])  # <-- Remove this and uncomment the code below to activate more than 2 Floating Point... """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....
                # only_two_start_num = cents_int
                print(only_two_start_num, '<-- for Testing')
                cent_int = list(map(int, str(only_two_start_num)))
                print(cent_int, '<-- get size')
                counting_cents_stored = len(cent_int)
                print(type(counting_cents_stored), '<-- count length')
                if counting_cents_stored == 1:
                    print(counting_cents_stored)
                    only_two_start_num = int(str(cents)[:2])
                    # only_two_start_num = cents_int
                    print(only_two_start_num, '<---- test print hhere')
                    cent_fraction = "{}0/100".format(only_two_start_num)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str.title())
                    self.word_for_journal_entries_val = test_str.title()
                else:
                    print(counting_cents_stored)
                    only_two_start_num = int(str(cents)[
                                             :2])  # <-- Remove this and uncomment the code below to activate more than 2 Floating Point... """PRINT STATEMENT IS JUST FOR TESTING PLEASE REMOVE IF YOU WANT""" ....
                    # only_two_start_num = cents_int
                    print(only_two_start_num, '<---- test print double')
                    only_two_start_num = int(str(cents)[:2])
                    cent_fraction = "{}/100".format(only_two_start_num)
                    word = "{} & {} Only".format(dollar_words, cent_fraction)
                    remove_and = re.sub(',', '', str(word))
                    remove_dash = re.sub('-', ' ', str(remove_and))
                    word_in_arr = remove_dash.split(' ')
                    print(re.sub('-', ' ', str(word_in_arr)), '<------- NEW')
                    test_str = ''
                    for rec_arr in word_in_arr:
                        if rec_arr != 'and':
                            test_str = test_str + rec_arr + ' '
                    print(test_str.title())
                    self.word_for_journal_entries_val = test_str.title()
            print('end test1')


class account_move_line(models.Model):
    _inherit = 'account.move.line'
    _description = 'Account Move Line Custom Inherit'

    debit_data_payable = fields.Float()
    credit_data_payable = fields.Float()
    debit_data = fields.Float()
    credit_data = fields.Float()
    to_debit_data = fields.Float()
    to_credit_data = fields.Float()
    to_debit_data_converted = fields.Float()
    to_credit_data_converted = fields.Float()
    debit_data_v2 = fields.Float()
    credit_data_v2 = fields.Float()
