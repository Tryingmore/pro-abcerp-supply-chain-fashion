/** @odoo-module **/

import {ActionDialog} from "@web/webclient/actions/action_dialog";
import {patch} from "@web/core/utils/patch";
import rpc from "web.rpc";
const {Component} = owl;
//const {onMounted} = owl.hooks;
import { usePosition } from "@web/core/position_hook";

export class ExpandButton extends Component {
    setup() {

        this.is_full = this.props.getsize();
        this.config = rpc.query({
            model: "ir.config_parameter",
            method: "get_web_dialog_size_config",
        });

        usePosition(() => {
            var self = this;
            this.config.then(function (r) {
                if (r.default_maximize && stop) {
                    self.dialog_button_extend();
                }
            });
        });
    }

    dialog_button_extend(event) {
        this.props.setsize("dialog_full_screen");
    }

    dialog_button_restore(event) {
      // 原本里面写的是this.last_size  我不知道是干啥的  要是其他的地方出了问题就恢复为this.last.size
        this.props.setsize('dialog_restore_size');
    }
}

ExpandButton.template = "web_dialog_size.ExpandButton";

Object.assign(ActionDialog, {
   components: {
        ...ActionDialog.components,
        ExpandButton,
    },
});

patch(ActionDialog.prototype, "web_dialog_size.ActionDialog", {
    setup() {
        this._super(...arguments);
        this.setSize = this.setSize.bind(this);
        this.getSize = this.getSize.bind(this);
    },

     _extending: function () {
        var dialog = this.modalRef.el.childNodes[0];
        dialog.classList.add('dialog_full_screen');

        $(".dialog_button_restore").hide()
        $(".dialog_button_extend").show()

    },

    _restore: function () {

        var dialog = this.modalRef.el.childNodes[0];
        dialog.classList.remove('dialog_full_screen');
        $(".dialog_button_restore").show()
        $(".dialog_button_extend").hide()
    },

    setSize(size) {
        if (size == 'dialog_full_screen') {
            this.size = 'dialog_full_screen';
            this._extending()
        }else if (size == 'dialog_restore_size') {
            this.size = 'dialog_restore_size'
            this._restore()
        }
        else {
            this.size = size;
            this.render();
        }

    },

    getSize() {
        return this.size;
    },
});



