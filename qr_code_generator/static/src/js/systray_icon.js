/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
console.log('systray update')
class SystrayIcon extends Component {
   setup() {
       super.setup(...arguments);
       this.action = useService("action");
   }
   _onClick() {
   console.log(this.env.services.popup.add(, {
   title:'warning'}))
   }
}
   SystrayIcon.template = "qr_code_generator.systray_icon";
   export const systrayItem = { Component: SystrayIcon};
   registry.category("systray").add("systray_icon", systrayItem, { sequence: 3 });
