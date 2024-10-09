# -*- coding: utf-8 -*-

from odoo import tests
from odoo.tests.common import HttpCase, TransactionCase, SingleTransactionCase, SavepointCase, Form
from odoo.exceptions import ValidationError
from werkzeug.urls import url_encode
from lxml import html as lxml_html
import json, datetime, os, sys, html, shutil

    
@tests.tagged('post_install', '-at_install')
class TestIrActionsReport(HttpCase):
    
    @classmethod
    def setUpClass(cls):
        super(TestIrActionsReport, cls).setUpClass()

    def setUp(cls):
        super(TestIrActionsReport, cls).setUp()
        cls.authenticate('admin', 'admin')
        cls.model_ids = cls.env['ir.model'].search([('model','ilike','ir.model')], limit=10)
        cls.model_ids_str = ','.join(cls.model_ids.mapped(lambda x: str(x.id)))

        resp = cls.url_open(url='/web/login')
        doc = lxml_html.fromstring(resp.text)
        cls.csrf_token = doc.xpath("//input[@name='csrf_token']")[0].get('value')

    def test_01_invalid_report_path(self):
        with self.assertRaises(ValidationError):
            self.env.ref('report_excel.report_ir_model_demo').write({
                'template_path': 'report_excel/demo/ir_model_demo11.xlsx'
            })

    def test_02_download_single_report(self):
        payload = {
            'data': json.dumps(['/report/excel/report_ir_model_demo/%s' % self.model_ids[0].id, 'qweb-excel']),
            'token': 'dummy-because-api-expects-one',
            'csrf_token': self.csrf_token
        }
        resp = self.url_open('/report/download', data=payload, timeout=30)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['content-type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_03_download_multi_report(self):
        self.env.ref('report_excel.report_ir_model_demo').write({'multi': False})
        payload = {
            'data': json.dumps(['/report/excel/report_ir_model_demo/%s' % self.model_ids_str, 'qweb-excel']),
            'token': 'dummy-because-api-expects-one',
            'csrf_token': self.csrf_token
        }
        resp = self.url_open('/report/download', data=payload, timeout=30)
        res = html.unescape(resp.text).encode('utf-8').decode('unicode_escape')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('当前报表的设置不支持同时输出多个单据', res)

    def test_04_download_report(self):
        payload = {
            'data': json.dumps(['/report/excel/report_ir_model_demo/%s' % self.model_ids_str, 'qweb-excel']),
            'token': 'dummy-because-api-expects-one',
            'csrf_token': self.csrf_token
        }
        resp = self.url_open('/report/download', data=payload, timeout=30)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['content-type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_05_download_not_exists_report(self):
        payload = {
            'data': json.dumps(['/report/excel/report_ir_model_demo_invalid/%s' % self.model_ids_str, 'qweb-excel']),
            'token': 'dummy-because-api-expects-one',
            'csrf_token': self.csrf_token
        }
        resp = self.url_open('/report/download', data=payload, timeout=30)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Invalid report name', resp.text)

    def test_06_download_report_with_context(self):
        params = {
            'docids': self.model_ids_str,
            'context': json.dumps({'active_id': 1, 'lang': 'zn_CN'})
        }
        payload = {
            'data': json.dumps(['/report/excel/report_ir_model_demo?%s' % url_encode(params), 'qweb-excel']),
            'token': 'dummy-because-api-expects-one',
            'csrf_token': self.csrf_token
        }
        resp = self.url_open('/report/download', data=payload, timeout=30)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['content-type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_07_download_report_without_docids(self):
        payload = {
            'data': json.dumps(['/report/excel/report_ir_model_demo/', 'qweb-excel']),
            'token': 'dummy-because-api-expects-one',
            'csrf_token': self.csrf_token
        }
        resp = self.url_open('/report/download', data=payload, timeout=30)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Can not find documents with empty doc ids', resp.text)

    def test_08_download_report_without_docids(self):
        params = {
            # 'docids': self.model_ids_str,
            'context': json.dumps({'active_id': 1, 'lang': 'zn_CN'})
        }
        payload = {
            'data': json.dumps(['/report/excel/report_ir_model_demo?%s' % url_encode(params), 'qweb-excel']),
            'token': 'dummy-because-api-expects-one',
            'csrf_token': self.csrf_token
        }
        resp = self.url_open('/report/download', data=payload, timeout=30)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Can not find documents with empty doc ids', resp.text)

    def test_09_download_report_multi(self):
        payload = {
            'data': json.dumps(['/report/excel/report_ir_model_multi_demo/%s' % self.model_ids_str, 'qweb-excel']),
            'token': 'dummy-because-api-expects-one',
            'csrf_token': self.csrf_token
        }
        resp = self.url_open('/report/download', data=payload, timeout=30)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers['content-type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
