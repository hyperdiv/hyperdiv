import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onSwitchChange = new EventHandler("sl-change", (key, evt) => {
  evt.stopPropagation();
  const checked = evt.target.checked;
  websocket.sendUpdate([key, "checked", checked], [key, "changed", true]);
});

export class Switch extends ShoelaceComponent {
  static eventHandlers() {
    return [onSwitchChange];
  }
}
