/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState, useRef, onWillStart} from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
console.log('Systray')
class SystrayIcon extends Component {
   setup() {
       super.setup(...arguments);
       this.action = useService("action");
       this.orm = useService("orm");
       this.inputRef = useRef('qr_input');
       this.imageRef = useRef("qr_image");
       this.state = useState({
       qrData :[],   })

   onWillStart(async () => {
        await this._qrReset();
   })
}
async _qrGenerate(input){
    var image = this.imageRef.show
    var input_value=this.inputRef.el.value
    self = this
        await this.orm.call('qr.model.wizard', 'generate_qr_code', [input_value],
        {}).then(function(result){
         var qr_dict = {}
         qr_dict['qr'] = result.qr_image
         self.state.qrData = qr_dict
    })
}
_qrReset(){

    var image = this.imageRef.hide
    this.state.qrData = []
}
}


   SystrayIcon.template = "systray_icon";
   SystrayIcon.components = {Dropdown};
   export const systrayItem = { Component: SystrayIcon,};
   registry.category("systray").add("SystrayIcon", systrayItem, { sequence: 500 });
