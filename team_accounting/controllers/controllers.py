from odoo.addons.web.controllers.main import ReportController
import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape


class PrtReportController(ReportController):
    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token, context=None):
        res = super(PrtReportController, self).report_download(data, token, context)
        if json.loads(data)[2] in ('open', 'print'):
            res.headers['Content-Disposition'] = res.headers['Content-Disposition'].replace('attachment', 'inline')
        return res


class TBXLSXReportController(http.Controller):
    @http.route('/dynamic_xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, token, report_data, report_name, dfr_data, **kw):

        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        dfr_data = dfr_data
        options = options
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_obj.get_dynamic_xlsx_report(options, response, report_data, dfr_data)
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))


