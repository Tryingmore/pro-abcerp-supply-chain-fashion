# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models,api,fields


class StockRule(models.Model):

    _inherit = "stock.rule"

    def _get_stock_move_values(self,product_id,product_qty,product_uom,location_dest_id,name,origin,company_id,values):
        move_values = super(StockRule, self)._get_stock_move_values(
            product_id,product_qty,product_uom,location_dest_id,name,origin,company_id,values,
        )
        sol_id = move_values.get("sale_line_id", False)
        if sol_id:
            sol_model = self.env["sale.order.line"]
            sol = sol_model.browse(sol_id)
            analytic_distribution = sol.analytic_distribution
            if analytic_distribution:
                move_values.update({"analytic_distribution": analytic_distribution})
        return move_values


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    analytic_account_ids = fields.Many2many(
        "account.analytic.account",compute="_compute_analytic_account_ids", store=True
    )

    @api.depends("analytic_distribution")
    def _compute_analytic_account_ids(self):
        for record in self:
            if not record.analytic_distribution:
                record.analytic_account_ids = False
            else:
                record.update(
                    {
                        "analytic_account_ids": [
                            (6, 0, [int(k) for k in record.analytic_distribution])
                        ]
                    }
                )

