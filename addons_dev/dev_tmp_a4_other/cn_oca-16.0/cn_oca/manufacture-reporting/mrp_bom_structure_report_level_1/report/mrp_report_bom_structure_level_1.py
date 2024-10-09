# © Copyright 2017-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, models


class MRPBomStructureReportLevel1(models.AbstractModel):
    _name = "report.mrp_bom_structure_report_level_1.mrp_bs_l1"
    _inherit = "report.mrp.report_bom_structure"
    _description = "BOM Structure Report Level 1"

    def _get_pdf_line(
        self, bom_id, product_id=False, qty=1, child_bom_ids=None, unfolded=False
    ):

        if child_bom_ids is None:
            child_bom_ids = []

        if self.env.context.get('warehouse'):
            warehouse = self.env['stock.warehouse'].browse(self.env.context.get('warehouse'))
        else:
            warehouse = self.env['stock.warehouse'].browse(self.get_warehouses()[0]['id'])
        if product_id:
            product = self.env['product.product'].browse(product_id)
        else:
            product = self.env['product.product']
        bom = self.env['mrp.bom'].browse(bom_id)
        data = self._get_bom_data(bom, warehouse, product=product, line_qty=qty, level=0)

        for comp in data['components']:
            comp['components'] = []
        pdf_lines = self._get_bom_array_lines(data, 1, set(), unfolded, True)

        data["components"] = []
        data["lines"] = pdf_lines
        return data
