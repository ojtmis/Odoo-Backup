from odoo import fields, models, api


class PayableVoucherXlsx(models.AbstractModel):
    _name = 'report.team_accounting.payable_voucher_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format2 = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': False})
        sheet = workbook.add_worksheet('PAYABLE VOUCHER')

        sheet.write(0, 4, 'TEAM PACIFIC CORPORATION', format2)
        sheet.write(1, 4, "VOUCHER'S PAYABLE", format2)

        sheet.write(2, 0, 'APV NO.:', format2)
        sheet.write(2, 5, 'VP DATE', format2)

        sheet.write(2, 1, 'PAYEE', format2)
        sheet.write(2, 2, 'ADMINISTRATOR', format2)
        sheet.write(3, 5, 'TIN', format2)
        sheet.write(3, 1, 'ADDRESS', format2)
        sheet.write(3, 2, 'ADDRESS', format2)
        sheet.write(3, 5, 'TRAN/INVOICE DATE', format2)
        sheet.write(3, 6, 'TRAN/INVOICE DATE', format2)

        sheet.write(4, 0, 'CURRENCY', format2)
        sheet.write(4, 1, 'USD', format2)
        sheet.write(4, 2, 'INV/REF# 000033', format2)
        sheet.write(4, 5, 'DUE DATE', format2)

        sheet.write(6, 0, 'IN PAYMENT OF THE FOLLOWING:', format2)

        sheet.write(8, 4, 'PARTICULAR EXPLANATION', format2)


        count_col = 0
        add_col = 1
        for x in lines.line_ids:
            sheet.write(10, count_col, x.name, format2)
            count_col += add_col

        count_col = 2
        add_col = 1
        for x in lines.line_ids:
            sheet.write(10, count_col, x.quantity, format2)
            count_col += add_col











