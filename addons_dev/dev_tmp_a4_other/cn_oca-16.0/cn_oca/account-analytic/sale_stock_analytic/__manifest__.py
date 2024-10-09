# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Stock Analytic",
    "summary": """
        Copies the analytic_distribution of the sale order line to the stock move""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-analytic",
    "data": ["views/sale_order_line_views.xml"],
    "depends": ["sale_stock", "stock_analytic"],
}
