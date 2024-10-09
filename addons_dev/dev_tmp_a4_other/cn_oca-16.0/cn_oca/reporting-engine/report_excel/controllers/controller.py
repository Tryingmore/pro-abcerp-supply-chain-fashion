# -*- coding: utf-8 -*-

import json
import os
from werkzeug.urls import url_decode
from odoo import http
from odoo.http import request, content_disposition
from odoo.tools.safe_eval import safe_eval, wrap_module
from odoo.tools import html_escape
from odoo.exceptions import ValidationError
from odoo.addons.web.controllers.report import ReportController
from odoo.http import serialize_exception as _serialize_exception

EXCEL_CONTENT_TYPE = {
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'xlsm': 'application/vnd.ms-excel.sheet.macroEnabled.12',
    'xltm': 'application/vnd.ms-excel.template.macroEnabled.12'
}

class ExcelReportController(ReportController):

    @http.route([
        '/report/<converter>/<reportname>',
        '/report/<converter>/<reportname>/<docids>',
    ], type='http', auth='user', website=True)
    def report_routes(self, reportname, docids=None, converter=None, **data):
        if converter == 'excel':
            report = request.env['ir.actions.report']._get_report_from_name(reportname)
            if not report:
                raise ValidationError('Invalid report name：%s' % reportname)
            context = dict(request.env.context)

            if docids:
                docids = [int(i) for i in docids.split(',')]
            else:
                docids = data.get('docids', None)
            if not docids:
                raise ValidationError('Can not find documents with empty doc ids!')

            if data.get('context'):
                # Ignore 'lang' here, because the context in data is the one from the webclient *but* if
                # the user explicitely wants to change the lang, this mechanism overwrites it.
                data['context'] = json.loads(data['context'])
                if data['context'].get('lang'):
                    del data['context']['lang']
                context.update(data['context'])

            file_ext = os.path.splitext(report.template_path)[-1][1:]
            # 根据模板渲染文件
            excel = report.with_context(context).render_excel(docids, data=data)[0]
            # 返回文件并下载
            headers = [('Content-Type', EXCEL_CONTENT_TYPE.get(file_ext, EXCEL_CONTENT_TYPE['xlsx'])), ('Content-Length', len(excel))]
            return request.make_response(excel, headers=headers)
        else:       # pragma: no cover
            return super(ExcelReportController, self).report_routes(reportname, docids, converter, **data)

    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, context=None, token=None):
        requestcontent = json.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:
            if type in ['qweb-excel', 'excel']:
                converter, extension, pattern = 'excel', 'xlsx', '/report/excel/'
                reportname = url.split(pattern)[1].split('?')[0]

                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')

                if docids:
                    # Generic report:
                    response = self.report_routes(reportname, docids=docids, converter=converter)
                else:
                    if '?' not in url:
                        raise ValidationError('Can not find documents with empty doc ids!')
                    # Particular report:
                    data = url_decode(url.split('?')[1]).items()  # decoding the args represented in JSON
                    response = self.report_routes(reportname, converter=converter, **dict(data))

                report = request.env['ir.actions.report']._get_report_from_name(reportname)
                filename = "%s.%s" % (report.name, extension)

                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)
                    if report.print_report_name and len(obj) <= 1:
                        report_name = safe_eval(report.print_report_name, {'object': obj, 'time': wrap_module(__import__('time'), [])})
                        filename = "%s.%s" % (report_name, extension)
                response.headers.add('Content-Disposition', content_disposition(filename))
                response.set_cookie('fileToken', token)
                return response
            else:       # pragma: no cover
                return super(ExcelReportController, self).report_download(data, token)
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))