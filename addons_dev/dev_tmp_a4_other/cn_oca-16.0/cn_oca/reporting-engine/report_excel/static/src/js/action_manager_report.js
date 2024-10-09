odoo.define('yumtown.ReportActionManager', function (require) {
    "use strict";

var core = require('web.core');
var session = require('web.session');
var AbstractAction = require('web.AbstractAction');
var ControlPanelMixin = require('web.ControlPanelMixin');
var config = require('web.config');
var ajax = require('web.ajax');
var Dialog = require('web.Dialog');
var WebClient = require('web.WebClient');
var ActionManager = require('web.ActionManager');

var QWeb = core.qweb;
var _t = core._t;

ActionManager.include({

    _executeReportAction: function (action, options) {
        var self = this;
        if (action.report_type === 'excel') {
            return self._triggerDownload(action, options, 'excel');
        }else{
            return this._super.apply(this, arguments);
        }
    },

    _makeReportUrls: function (action) {
        var reportUrls = {
            html: '/report/html/' + action.report_name,
            pdf: '/report/pdf/' + action.report_name,
            text: '/report/text/' + action.report_name,
            excel: '/report/excel/' + action.report_name,
        };
        // We may have to build a query string with `action.data`. It's the place
        // were report's using a wizard to customize the output traditionally put
        // their options.
        if (_.isUndefined(action.data) || _.isNull(action.data) ||
            (_.isObject(action.data) && _.isEmpty(action.data))) {
            if (action.context.active_ids) {
                var activeIDsPath = '/' + action.context.active_ids.join(',');
                reportUrls = _.mapObject(reportUrls, function (value) {
                    return value += activeIDsPath;
                });
            }
        } else {
            var serializedOptionsPath = '?options=' + encodeURIComponent(JSON.stringify(action.data));
            serializedOptionsPath += '&context=' + encodeURIComponent(JSON.stringify(action.context));
            reportUrls = _.mapObject(reportUrls, function (value) {
                return value += serializedOptionsPath;
            });
        }
        return reportUrls;
    },
})

})