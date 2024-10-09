/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {Dialog} from "@web/core/dialog/dialog";
import {ActionDialog} from "@web/webclient/actions/action_dialog";
import { useExternalListener } from "@web/core/position_hook";
import { useListener } from "@web/core/utils/hooks";
const {Component} = owl;


export class DialogDraggable extends Component {

    setup() {
        this.element_position = {x: 0, y: 0};
        this.mouse_to_element_ratio = {x: 0, y: 0};
        const bound_onDrag = this.onDrag.bind(this);
        setTimeout(()=>{
           $('.modal-content')[0].addEventListener('mousedown',(event)=>{

               let disx =event.clientX -  $('.modal-content')[0].offsetLeft
               let disy =event.clientY -  $('.modal-content')[0].offsetTop
                $(document).on('mousemove',(event)=>{
                   let  x =  event.clientX- disx
                   let  y =  event.clientY - disy
                   var css = {
                      position :'absolute',
                      left : x+'px',
                      top :  y+'px'

                   }
                   $('.modal-content').css(css)

               })
               $(document).on('mouseup',()=>{
                  $(document).off()
               })
           })
        },100)

    }

    mounted() {

        this.el.classList.add("position-absolute");
        this.el.offsetParent.classList.add("position-relative");
    }
    getMovePosition({x, y}) {

        return {
            x: x - this.mouse_to_element_ratio.x - this.element_position.x,
            y: y - this.mouse_to_element_ratio.y - this.element_position.y,
        };
    }
    onDrag(event) {

        const {x, y} = this.getMovePosition(event);
        this.el.style.left = `${x}px`;
        this.el.style.top = `${y}px`;
    }
}

DialogDraggable.template = "DialogDraggable";

Object.assign(ActionDialog, {
   components: {
        ...ActionDialog.components,
        DialogDraggable,
    },
});
