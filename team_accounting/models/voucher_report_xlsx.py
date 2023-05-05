from odoo import fields, models, api


class VoucherReportXlsx(models.AbstractModel):
    _name = 'report.team_accounting.voucher_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 12.5, 'align': 'vcenter', 'bold': False})
        format3 = workbook.add_format({'font_size': 8.5, 'align': 'vcenter', 'bold': False})
        format4 = workbook.add_format({'font_size': 7.5, 'align': 'vcenter', 'bold': False})
        # format = workbook.add_format({'text-transform': 'uppercase'})
        format_name = workbook.add_format({'font_size': 12.5, 'align': 'vcenter', 'bold': False})

        sheet = workbook.add_worksheet('Voucher')

        sheet.write(0, 0, lines.payment_date.strftime('%B-%d-%Y'), format2)
        sheet.write(2, 1, lines.name, format3)
        sheet.write(2, 3, lines.amount, format4)
        sheet.write(4, 2, lines.communication, format3)
        sheet.write(37, 7, lines.payment_date.strftime('%m %d %Y'), format2)
        sheet.write(38, 1, lines.partner_id.name, format_name)
        sheet.write(39, 7, lines.amount, format2)
        sheet.write(39, 1, lines.word_move, format2)

        print(lines.move_line_ids.account_id)

        check_data = lines.move_line_ids

        count_debit_row = 11
        for x in check_data:
            sheet.write(count_debit_row, 7, x.debit, format2)
            count_debit_row += count_debit_row

        count_debit_row = 11
        for x in check_data:
            sheet.write(count_debit_row, 8, x.credit, format2)
            count_debit_row += count_debit_row

        check = lines.move_line_ids.account_id

        count_row = 11
        for x in check:
            sheet.write(count_row, 3, x.name, format2)
            count_row += count_row

        count_col = 2
        for x in check:
            sheet.write(25, count_col, x.name, format2)
            count_col += count_col



