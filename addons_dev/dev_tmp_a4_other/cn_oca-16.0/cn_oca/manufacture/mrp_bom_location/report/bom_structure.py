# Copyright 2017-20 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models


class BomStructureReport(models.AbstractModel):
    _inherit = "report.mrp.report_bom_structure"

    # @api.model
    # def get_html(self, bom_id=False, searchQty=1, searchVariant=False):
    #     res = super(BomStructureReport, self).get_html(bom_id, searchQty, searchVariant)
    #     return res

    # @api.model
    # def _get_pdf_doc(self, bom_id, data, quantity, product_variant_id=None):
    #     res = super(BomStructureReport, self)._get_pdf_doc(bom_id, data, quantity, product_variant_id)
    #     return res

    @api.model
    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        res = super(BomStructureReport, self)._get_bom_lines(
            bom, bom_quantity, product, line_id, level
        )
        line_ids = self.env["mrp.bom.line"].search([("bom_id", "=", bom.id)])
        for line in res[0]:
            line_id = line_ids.filtered(
                lambda l: l.location_id and l.id == line["line_id"]
            )
            line["location_id"] = line_id.location_id or ""
        return res

    @api.model
    def _get_pdf_line(self, bom_id, product_id=False, qty=1, unfolded_ids=None, unfolded=False):
        res = super(BomStructureReport, self)._get_pdf_line(bom_id, product_id, qty, unfolded_ids, unfolded)
        line_ids = self.env["mrp.bom.line"].search([("bom_id", "=", bom_id)])
        for line in res["lines"]:
            line_id = line_ids.filtered(lambda l: l.location_id and l.product_id.display_name == line["name"])
            line["location_name"] = line_id.location_id.complete_name or ""
        return res

    @api.model
    def _get_component_data(self, parent_bom, warehouse, bom_line, line_quantity, level, index, product_info, ignore_stock=False):
        res = super(BomStructureReport, self)._get_component_data(parent_bom, warehouse, bom_line, line_quantity, level, index, product_info, ignore_stock)
        res['location_id'] = bom_line.location_id.id
        res['location_name'] = bom_line.location_id.complete_name or ""
        res['location_model'] = bom_line.location_id._name
        return res
