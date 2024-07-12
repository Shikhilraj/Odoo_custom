/** @odoo-module */
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";
console.log('Orderline')
patch(Orderline.prototype, {
    removeLine() {
     console.log(this.props)
        const order = this.env.services.pos.get_order();
        const orderline = order.orderlines.find((line) => line.full_product_name == this.props.line.productName)
//          const orderline = order.orderlines.find((line) => line.id)
        return order.removeOrderline(orderline);
    }

})