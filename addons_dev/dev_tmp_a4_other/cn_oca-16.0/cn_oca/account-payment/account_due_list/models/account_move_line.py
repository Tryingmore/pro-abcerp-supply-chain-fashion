# © 2008 Zikzakmedia S.L. (http://zikzakmedia.com)
#        Jordi Esteve <jesteve@zikzakmedia.com>
# © 2011 Domsense srl (<http://www.domsense.com>)
# © 2011-2013 Agile Business Group sagl (<http://www.agilebg.com>)
# © 2015 Andrea Cometa <info@andreacometa.it>
# © 2015 Eneko Lacunza <elacunza@binovo.es>
# © 2015 Tecnativa (http://www.tecnativa.com)
# © 2016 ForgeFlow S.L. (http://www.forgeflow.com)
# © 2018 Ozono Multimedia S.L.L.
#        (http://www.ozonomultimedia.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models,api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    invoice_origin = fields.Char(related="move_id.invoice_origin", string="Source Doc")
    invoice_date = fields.Date(related="move_id.invoice_date", string="Invoice Date")
    partner_ref = fields.Char(related="partner_id.ref", string="Partner Ref")
    payment_term_id = fields.Many2one(
        "account.payment.term",
        related="move_id.invoice_payment_term_id",
        string="Payment Terms",
    )
    invoice_user_id = fields.Many2one(
        comodel_name="res.users",
        related="move_id.invoice_user_id",
        string="Invoice salesperson",
        store=True,
    )

    @api.model
    def get_view(
            self, view_id=None, view_type="form", **options
    ):
        model_data_obj = self.env["ir.model.data"].sudo()
        ids = model_data_obj.search(
            [("module", "=", "account_due_list"), ("name", "=", "view_payments_tree")]
        )
        if ids:
            view_payments_tree_id = model_data_obj._xmlid_to_res_id(
                "account_due_list.view_payments_tree"
            )
        if ids and view_id == view_payments_tree_id:
            # Use due list
            result = super(models.Model, self).get_view(
                view_id, view_type, **options
            )
        else:
            # Use special views for account.move.line object
            # (for ex. tree view contains user defined fields)
            result = super(AccountMoveLine, self).get_view(
                view_id, view_type, **options
            )
        return result