/** @odoo-module */
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";
console.log("clear")

export class ButtonClear extends Component {
    static template = "pos_order_line_remove.ButtonClear";

    setup() {
        this.pos = usePos();
        }
    click() {
        const order = this.pos.get_order();
        const orderlines=order.orderlines;
        const orderLineLength = orderlines.length
        var j=0
        for(var i=0 ;i<orderLineLength;i++){
        if(orderlines.length != 0){ order.removeOrderline(orderlines[j]) }
        }
    }
}
    ProductScreen.addControlButton({
    component: ButtonClear,
    position: ["after", "OrderlineCustomerNoteButton"],
});

