/** @odoo-module **/
import { parse, evaluate, evaluateExpr, tokenize  } from "@web/core/py_js/py";
import { BUILTINS as PYBUILTINS } from "@web/core/py_js/py_builtin";
import { patch } from "@web/core/utils/patch";
import { ListRenderer } from "@web/views/list/list_renderer";

patch(ListRenderer.prototype, "web_tree_dynamic_colored_field", {
        /**
         * Colorize the current cell depending on expressions provided.
         *
         * @param {Element} $td a <td> tag inside a table representing a list view
         * @param {Object} record
         * @param {Object} node an XML node (must be a <field>)
         * @param {Object} ctx evaluation context for the record
         */
         getCellStyle(column, record) {
            if (column.type !== 'field'){
                return;
            }
            const { rawAttrs } = this.props.list.activeFields[column.name];
            if (!rawAttrs.options) {
                return;
            }
            var cellOptions = rawAttrs.options;
            if (!_.isObject(cellOptions)) {
                cellOptions = evaluateExpr(cellOptions, record.data);
            }
            let ctx = this.getEvalContext(record);
            let cellStyle = ""
            cellStyle = this.applyColorizeHelper(cellStyle, cellOptions, "fg_color", "color", ctx);
            cellStyle = this.applyColorizeHelper(cellStyle, cellOptions, "bg_color", "background-color", ctx);
            return cellStyle;
        },

        /**
         * @param {Element} $td a <td> tag inside a table representing a list view
         * @param {Object} nodeOptions a mapping of nodeOptions parameters to the color itself
         * @param {Object} node an XML node (must be a <field>)
         * @param {String} nodeAttribute an attribute of a node to apply a style onto
         * @param {String} cssAttribute a real CSS-compatible attribute
         * @param {Object} ctx evaluation context for the record
         */
        applyColorizeHelper (
            nodeStyle,
            nodeOptions,
            nodeAttribute,
            cssAttribute,
            ctx
        ) {
            if (nodeOptions[nodeAttribute]) {
                var colors = _(nodeOptions[nodeAttribute].split(";"))
                    .chain()
                    .map(this.pairColors)
                    .value()
                    .filter(function CheckUndefined(value) {
                        return value !== undefined;
                    });
                for (var i = 0, len = colors.length; i < len; ++i) {
                    var pair = colors[i],
                        color = pair[0],
                        expression = pair[1];
                    try{
                        if (evaluate(expression, ctx)) {
                            nodeStyle += cssAttribute + ":" + color + ";"
                            return nodeStyle;
                        }                        
                    } catch (e){
                        console.log('web_tree_dynamic_colored_field', e);
                    }
                }
            }
            return nodeStyle;
        },

        /**
         * Parse `<color>: <field> <operator> <value>` forms to
         * evaluable expressions
         *
         * @param {String} pairColor `color: expression` pair
         * @returns {Array} undefined or array of color, parsed expression,
         * original expression
         */
        pairColors (pairColor) {
            if (pairColor !== "") {
                var pairList = pairColor.split(":"),
                    color = pairList[0],
                    // If one passes a bare color instead of an expression,
                    // then we consider that color is to be shown in any case
                    expression = pairList[1] ? pairList[1] : "True";
                return [color, parse(tokenize(expression)), expression];
            }
            return undefined;
        },  
        
        /**
         * Construct domain evaluation context, mostly by passing
         * record's fields's values to local scope.
         *
         * @param {Object} record a record to build a context from
         * @returns {Object} evaluation context for the record
         */
         getEvalContext(record) {
            var ctx = _.extend({}, record.data, PYBUILTINS);
            for (var key in ctx) {
                var value = ctx[key];
                if (ctx[key] instanceof moment) {
                    // Date/datetime fields are represented w/ Moment objects
                    // docs: https://momentjs.com/
                    ctx[key] = value.format("YYYY-MM-DD hh:mm:ss");
                }
            }
            return ctx;
        },        

})
