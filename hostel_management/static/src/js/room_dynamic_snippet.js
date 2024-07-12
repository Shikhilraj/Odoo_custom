/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import {jsonrpc} from "@web/core/network/rpc_service";
import {renderToFragment} from "@web/core/utils/render";
export function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

var Dynamic = PublicWidget.Widget.extend
({
    selector: '.latest_room_snippet',
    willStart: async function() {
        await jsonrpc('/new_rooms', ).then((data) => {
            this.data = data;
        });
    },
    start: function() {
        var index = Date.now()
        if (this.data == null){
            window.alert('There is no data');
            return false
        }
        var refl = this.$el.find('#latest_room_carousel')
        const chunks = chunk(this.data, 4)
        chunks[0].is_active = true
        refl.html(renderToFragment('hostel_management.room_snippet_carousel',
         {
            'chunks': chunks,
            'index': index
         }
            )
        )
    },
    });

    PublicWidget.registry.LatestRoom = Dynamic;
    return Dynamic;






























