/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { BomOverviewDisplayFilter } from "@mrp/components/bom_overview_display_filter/mrp_bom_overview_display_filter";

patch(BomOverviewDisplayFilter.prototype, "constructor", {
    setup() {
        this._super(...arguments);
        this.displayOptions.location = this.env._t('Location');
    },
});
