from odoo import fields, models, api


class PaymentVoucherXlsx(models.AbstractModel):
    _name = 'report.team_accounting.payment_voucher_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Payment Voucher Xlsx'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 12.5, 'align': 'vcenter', 'bold': False})
        format3 = workbook.add_format({'font_size': 8.5, 'align': 'vcenter', 'bold': False})
        format4 = workbook.add_format({'font_size': 7.5, 'align': 'vcenter', 'bold': False})
        sheet = workbook.add_worksheet('Payment Voucher')

        sheet.write(0, 0, 'Date: ', format2)
        sheet.write(0, 1, lines.payment_date.strftime('%m %d %Y'), format2)
        sheet.write(1, 0, 'INV DATE', format2)
        sheet.write(1, 1, 'RCP#', format2)
        sheet.write(1, 2, 'PV#', format2)
        sheet.write(1, 3, 'PO#', format2)
        sheet.write(1, 4, 'INVOICE', format2)
        sheet.write(1, 5, 'AMOUNT', format2)
        sheet.write(1, 6, 'INV DATE', format2)
        sheet.write(1, 7, 'RCP#', format2)
        sheet.write(1, 8, 'PV#', format2)
        sheet.write(1, 9, 'PO#', format2)
        sheet.write(1, 10, 'AMOUNT', format2)

        if not lines.communication:
            sheet.write(2, 0, 'No DATA', format2)
        else:
            sheet.write(2, 0, lines.communication, format2)

        sheet.write(2, 1, '', format2)
        sheet.write(2, 2, '', format2)
        sheet.write(2, 3, '', format2)
        sheet.write(2, 4, '', format2)
        sheet.write(2, 5, lines.invoice_ids.amount_total, format2)
        sheet.write(2, 6, '', format2)
        sheet.write(2, 7, '', format2)
        sheet.write(2, 8, '', format2)
        sheet.write(2, 9, '', format2)
        sheet.write(2, 10, '', format2)

        sheet.write(8, 3, 'TOTAL: ', format2)
        sheet.write(8, 4, lines.invoice_ids.amount_total, format2)

        sheet.write(10, 0, 'ACC. DEBIT', format2)
        sheet.write(10, 2, 'ACC. CREDIT', format2)
        sheet.write(10, 4, 'ACC. NAME', format2)
        sheet.write(10, 8, 'DEBIT', format2)
        sheet.write(10, 10, 'DEBIT', format2)

        check_data = lines.move_line_ids
        plus = 1

        sheet.write(11, 0, 'ACC. DEBIT', format2)
        sheet.write(11, 2, 'ACC. CREDIT', format2)

        count_name_row = 11
        for x in check_data:
            sheet.write(count_name_row, 4, x.account_id.name, format2)
            count_name_row += plus

        count_debit_row = 11
        for x in check_data:
            sheet.write(count_debit_row, 8, x.debit, format2)
            count_debit_row += plus

        count_credit_row = 11
        for x in check_data:
            sheet.write(count_credit_row, 10, x.credit, format2)
            count_credit_row += plus

        sheet.write(15, 2, 'Particulars', format2)

        check_data = lines.move_line_ids
        plus = 1
        count_name_row = 15
        for x in check_data:
            sheet.write(count_name_row, 3, x.account_id.name, format2)
            count_name_row += plus

        sheet.write(18, 4, '------------------', format2)
        sheet.write(19, 4, 'PREPARED BY', format2)

        sheet.write(18, 8, '------------------', format2)
        sheet.write(19, 8, 'APPROVED BY', format2)

        sheet.write(20, 4, '------------------', format2)
        sheet.write(21, 4, 'CHECKED BY', format2)

        sheet.write(20, 5, '------------------', format2)
        sheet.write(21, 5, 'PREPARED BY', format2)
        sheet.write(20, 8, '------------------', format2)
        sheet.write(21, 8, 'PREPARED BY', format2)

        sheet.write(23, 0, 'TEAM PACIFIC CORPORATION ')
        sheet.write(23, 6, 'CHECK NO.')

        if not lines.communication:
            sheet.write(23, 10, 'No DATA', format2)
        else:
            sheet.write(23, 10, lines.communication, format2)

        sheet.write(24, 10, lines.payment_date.strftime('%m %d %Y'), format2)

        sheet.write(25, 2, lines.partner_id.name, format2)
        sheet.write(26, 2, lines.word_num, format2)
        sheet.write(26, 10, lines.amount, format2)

        sheet.write(28, 2, 'Paying Bank', format2)

        check_data_bank = lines.partner_bank_account_id
        plus = 1
        count_bank_row = 29
        for x in check_data_bank:
            if not check_data_bank:
                sheet.write(29, 2, 'No DATA', format2)
            else:
                sheet.write(count_bank_row, 2, x.name, format2)
            count_bank_row += plus

















