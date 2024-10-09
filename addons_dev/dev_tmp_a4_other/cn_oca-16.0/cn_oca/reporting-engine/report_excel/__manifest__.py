# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Base excel report",
    "summary": "Use excel template to generate excel report",
    "author": "feihu.zhang<feihu.zhang@live.com>" "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/reporting-engine",
    "category": "Reporting",
    "version": "16.0.1.1.1",
    "development_status": "Mature",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [
            "openpyxl"          # pip3 install openpyxl==3.1.2
        ]
    },
    "data": [
        "views/ir_actions_report_views.xml",
    ],
    "depends": ["base", "web"],
    "demo": [
        "demo/ir_actions_report.xml"
    ],
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "report_excel/static/src/js/report/action_manager_report.esm.js"
        ],
    },
}
