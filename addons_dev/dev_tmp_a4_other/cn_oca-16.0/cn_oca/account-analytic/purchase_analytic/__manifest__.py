# © 2016  Laetitia Gangloff, Acsone SA/NV (http://www.acsone.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Analytic",
    "summary": """
        This module add analytic distribution on purchase order.
        If all lines of the purchase order have the same analytic distribution, 
        the analytic distribution on the purchase order is automatically set with this value.
        If a analytic distribution is set on the purchase order, 
        all lines of the purchase will take this value.""",
    "version": "16.0.1.0.0",
    "author": "Acsone SA/NV, Odoo Community Association (OCA)",
    "category": "Purchase Management",
    "website": "https://github.com/OCA/account-analytic",
    "depends": ["purchase"],
    "data": ["views/purchase_views.xml"],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
}
