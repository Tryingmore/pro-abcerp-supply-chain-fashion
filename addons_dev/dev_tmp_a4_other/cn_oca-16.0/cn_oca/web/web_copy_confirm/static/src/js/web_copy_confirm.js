/** @odoo-module **/

// Copyright (C) 2018 DynApps <http://www.dynapps.be>
// Copyright (C) 2022 Yizuo <https://www.yizuo.ltd>
// @author Stefan Rijnhart <stefan@opener.amsterdam>
// @author Robin Conjour <rconjour@demolium.com>
// PengYB(YiZuo) use OWL Rewrite.
// @author PengYB <pengyb@yizuo.ltd>
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import { FormController } from "@web/views/form/form_controller";
import { _lt } from "@web/core/l10n/translation";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { patch } from "@web/core/utils/patch";

patch(FormController.prototype,"Duplicate Confirm",{

    async duplicateRecord() {
        const dialogProps = {
            body: _lt("Are you sure that you would like to copy this record?"),
            confirm: async () => {
                await this.model.root.duplicate();
//                if (!this.model.root.resId) {
//                    this.env.config.historyBack();
//                }
            },
            cancel: () => {},
        };
        this.dialogService.add(ConfirmationDialog, dialogProps);
    }
});