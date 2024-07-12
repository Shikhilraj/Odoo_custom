/** @odoo-module */
import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { roundDecimals as round_di } from "@web/core/utils/numbers";
patch(Orderline.prototype, {
    getDisplayData() {
        return {
            ...super.getDisplayData(),
            discount_prize: this.product.discount_prize,
        };
    },
    get_unit_price() {
        super.get_unit_price()
        var digits = this.pos.dp["Product Price"];
        var PriceWithDiscount = this.price - this.product.discount_prize
        // round and truncate to mimic _symbol_set behavior
    return parseFloat(round_di(PriceWithDiscount || 0, digits).toFixed(digits));
    }
});

