# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models,api,fields


class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

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


    def _prepare_stock_moves(self, picking):
        res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking)
        for line in res:
            analytic_distribution = self.analytic_distribution
            if analytic_distribution:
                line.update({"analytic_distribution": analytic_distribution})
        return res
