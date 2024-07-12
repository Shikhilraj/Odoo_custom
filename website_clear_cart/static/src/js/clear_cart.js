/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

PublicWidget.registry.LatestRoom = PublicWidget.Widget.extend
({
    selector: '.oe_website_sale',
    events: {
        'click #products_clear_button':'_onButtonClick',
    },
    _onButtonClick: async function(ev){
        await jsonrpc('/website_sale/clear_cart', )
        window.location.reload();
    },
})
