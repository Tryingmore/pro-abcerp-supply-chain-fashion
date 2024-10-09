# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "MRP BOM Location",
    "summary": "Adds location field to Bill of Materials and its components.",
    "version": "16.0.1.0.0",
    "category": "Manufacture",
    "website": "https://github.com/OCA/manufacture",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "depends": ["mrp"],
    'assets': {
        'web.assets_backend': [
            # 'mrp_bom_location/static/src/bom_overview/mrp_bom_overview_display_filter.js',
            'mrp_bom_location/static/src/bom_overview/mrp_bom_overview_table.js',
            'mrp_bom_location/static/src/bom_overview/mrp_bom_overview_table.xml',
            'mrp_bom_location/static/src/bom_overview/mrp_bom_overview_line.xml',
            'mrp_bom_location/static/src/bom_overview/mrp_bom_overview_special_line.xml',
        ],
    },

    "data": ["views/mrp_view.xml", "views/report_mrpbomstructure.xml"],
    "installable": True,
}
