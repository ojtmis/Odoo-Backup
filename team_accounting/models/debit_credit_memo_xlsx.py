from odoo import fields, models, api


class DebitCreditMemo(models.AbstractModel):
    _name = 'report.team_accounting.debit_credit_memo_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format2 = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': False})
        sheet = workbook.add_worksheet('DEBIT / CREDIT MEMO')

        #Header

        sheet.write(1, 4, 'DEBIT / CREDIT MEMO', format2)
        sheet.write(3, 0, 'Customer Code:', format2)

        check_data = lines.line_ids.partner_id
        count_row = 2
        for x in check_data:
            sheet.write(3, count_row, x.name, format2)
            count_row += count_row

        sheet.write(4, 0, 'For:', format2)
        sheet.write(4, count_row, lines.partner_id.street, format2)
        sheet.write(5, count_row, lines.partner_id.state_id.name, format2)
        sheet.write(6, count_row, lines.partner_id.country_id.name, format2)

        sheet.write(7, 0, 'In the amount of:', format2)
        sheet.write(8, 0, 'To apply to the following:', format2)

        sheet.write(3, 7, 'DM/CM no:', format2)
        sheet.write(3, 8, lines.name, format2)

        sheet.write(4, 7, 'Date:', format2)
        sheet.write(4, 8, lines.date.strftime('%m %d %Y'), format2)

        sheet.write(5, 7, 'Terms:', format2)
        sheet.write(5, 8, lines.invoice_payment_term_id.name, format2)

        sheet.write(6, 7, 'Due Date:', format2)

        #End

        sheet.write(10, 2, 'PARTICULARS', format2)
        sheet.write(10, 9, 'AMOUNT', format2)
        sheet.write(26, 9, lines.total_usd, format2)
        sheet.write(12, 0, 'TO DEBIT YOUR ACCOUNT FOR:', format2)

        check_data = lines.line_ids
        count_col = 1
        for x in check_data:
            sheet.write(14, count_col, x.name, format2)
            count_col += count_col

        sheet.write(17, 3, 'AMOUNT in: ', format2)
        sheet.write(17, 4, lines.currency_id.name, format2)
        sheet.write(17, 5, lines.amount_total_in_php, format2)
        sheet.write(18, 3, 'FOREX RATE: ', format2)
        sheet.write(18, 4, lines.forex_ex, format2)
        sheet.write(19, 4, '----------------------', format2)
        sheet.write(21, 3, 'AMOUNT US$ :', format2)
        sheet.write(21, 4, lines.total_amount_without_monetary, format2)
        sheet.write(22, 1, 'ADD: ', format2)
        sheet.write(22, 2, lines.percentage * 100, format2)
        sheet.write(22, 3, '% PROCESSING FEE :', format2)
        sheet.write(22, 4, lines.divided_usd, format2)
        sheet.write(23, 4, '----------------------', format2)
        sheet.write(24, 4, lines.total_usd, format2)
        sheet.write(24, 3, 'TOTAL US$:', format2)

        sheet.write(26, 0, 'AMOUNT IN WORDS: ', format2)
        sheet.write(26, 1, lines.word_num.upper() + ' ONLY', format2)

        sheet.write(30, 0, 'GL ENTRY', format2)

        sheet.write(33, 2, 'GL CODE', format2)
        sheet.write(33, 4, 'DESCRIPTION', format2)
        sheet.write(33, 6, 'DEBIT', format2)
        sheet.write(33, 8, 'CREDIT', format2)

        data_account_id = lines.line_ids.account_id
        data_debit_credit = lines.line_ids
        count_gl_row = 34
        plus = 1
        for x in data_account_id:
            sheet.write(count_gl_row, 2, x.code, format2)
            count_gl_row += plus

        count_gl_row = 34
        for x in data_account_id:
            sheet.write(count_gl_row, 4, x.name, format2)
            count_gl_row += plus

        count_gl_row = 34
        for x in data_debit_credit:
            sheet.write(count_gl_row, 6, x.debit, format2)
            count_gl_row += plus

        count_gl_row = 34
        for x in data_debit_credit:
            sheet.write(count_gl_row, 8, x.credit, format2)
            count_gl_row += plus

        sheet.write(40, 2, 'PREPARED BY:', format2)
        sheet.write(40, 4, 'CHECKED BY:', format2)
        sheet.write(40, 8, 'APPROVED BY:', format2)

































