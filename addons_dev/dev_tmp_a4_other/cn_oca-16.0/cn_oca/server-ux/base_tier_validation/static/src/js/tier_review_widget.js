/** @odoo-module **/

import {registry} from "@web/core/registry";
import {X2ManyField} from "@web/views/fields/x2many/x2many_field";

import {useService} from "@web/core/utils/hooks";

import {renderToMarkup, renderToText} from "@web/core/utils/render";
const {
    Component,
    onWillStart,
    onWillRender,
    onRendered,
    onPatched,
    useState,
    useSubEnv,
} = owl;

export class ReviewsTable extends Component {
    setup() {
        this.docs = useState({});
        var self = this;
        this.collapse = false;
        this.orm = useService("orm");
        this.reviews = [];
    }
    _getReviewData() {
        const records = this.env.model.root.data.review_ids.records;
        const reviews = [];
        for (var i = 0; i < records.length; i++) {
            reviews.push(records[i].data);
        }
        return reviews;
    }
    onToggleCollapse(ev) {
        var $panelHeading = $(ev.currentTarget).closest(".panel-heading");
        if (this.collapse) {
            $panelHeading.next("div#collapse1").hide();
        } else {
            $panelHeading.next("div#collapse1").show();
        }
        this.collapse = !this.collapse;
    }
}

ReviewsTable.template = "base_tier_validation.Collapse";
registry.category("fields").add("form.tier_validation", ReviewsTable);
