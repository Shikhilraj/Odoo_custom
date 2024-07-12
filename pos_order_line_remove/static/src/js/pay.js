/** @odoo-module */
import { Order } from "@point_of_sale/app/store/models";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype,{
async pay(){
   const order = this.pos.get_order();
   var orderlines=this.get_orderlines();
    var amount_total = 0;
    orderlines.forEach(element => {
    amount_total += element.price;
    })
    console.log(amount_total)
    if(amount_total > 1000 && this.env.services.user.hasGroup('point_of_sale.group_pos_manager')){
        super.pay(...arguments)
        }
    else{
        await this.env.services.popup.add(ErrorPopup, {
        title: _t('Warning'),
         body: _t("Please try again."),
         })
        console.log(this.env.services.user)
    }}

})