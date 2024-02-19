import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onCheckboxChange = new EventHandler("sl-change", (key, evt) => {
  evt.stopPropagation();
  const checked = evt.target.checked;
  websocket.sendUpdate(
    [key, "checked", checked],
    [key, "changed", true],
    [key, "indeterminate", false]
  );
});

export class Checkbox extends ShoelaceComponent {
  static eventHandlers() {
    return [onCheckboxChange];
  }
}
