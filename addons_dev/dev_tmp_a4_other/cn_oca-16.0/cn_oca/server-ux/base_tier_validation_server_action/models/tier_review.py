# Copyright 2020 Ecosoft (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class TierReview(models.Model):
    _inherit = "tier.review"


    def max_sequence_reviews(self):
        resource = self.env[self.model].browse(self.res_id)
        reviews = resource.review_ids.filtered(lambda r: r.status != "")
        if reviews:
            max_sequence = max(reviews.mapped("sequence"))
        else:
            max_sequence =-1
        return max_sequence

    def write(self, vals):
        res = super().write(vals)
        if vals.get("status") in ["approved", "rejected"]:
            for rec in self:
                server_action = False
                if rec.sequence==self.max_sequence_reviews():
                    if rec.status == "approved":
                        server_action = rec.definition_id.server_action
                if rec.status == "rejected":
                    server_action = rec.definition_id.rejected_server_action
                if server_action:
                    model = self.env[rec.model].browse(rec.res_id)
                    print(server_action)
                    for action in server_action.split('\n'):
                        eval(action)
        return res


    # def write(self, vals):
    #     res = super().write(vals)
    #     if vals.get("status") in ["approved", "rejected"]:
    #         for rec in self:
    #             server_action = False
    #             if rec.status == "approved":
    #                 server_action = rec.definition_id.server_action_id
    #             if rec.status == "rejected":
    #                 server_action = rec.definition_id.rejected_server_action_id
    #             server_action_tier = self.env.context.get("server_action_tier")
    #             # Don't allow reentrant server action as it will lead to
    #             # recursive behaviour
    #             if server_action and (
    #                 not server_action_tier or server_action_tier != server_action.id
    #             ):
    #                 server_action.with_context(
    #                     server_action_tier=server_action.id,
    #                     active_model=rec.model,
    #                     active_id=rec.res_id,
    #                 ).sudo().run()
    #     return res
