/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

console.log("Starting...")
publicWidget.registry.portalDetails = publicWidget.Widget.extend({
    selector: '.o_mark_required',
    events: {
        'change #dob': '_onAgeCalculation',
        'click #room_id':'_onDropdownClick',
    },

    _onAgeCalculation: function(){ //Age Calculation on dob field
        var dob = new Date($('#dob').val())
        let month = dob.getMonth()
        let year = dob.getFullYear()
        const now = new Date()
        var age = now.getFullYear() - year
        var month_diff = now.getMonth() - month
        if (month_diff < 0){
            age -=1
        }
    $('#age').val(age)
    },


    _onDropdownClick: function(){ // find the rent of given room
    var self = this;
    var room_id = $('#room_id').val()
    if (room_id){
        return jsonrpc('/hostel/room', {room_number : room_id}
        ).then((result) => {
            self.$el.find('#monthly_amount').val(result)
        });
    }
    },
})