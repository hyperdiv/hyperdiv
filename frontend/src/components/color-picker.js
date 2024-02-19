import debounce from "debounce";
import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onColorChange = new EventHandler(
  "sl-change",
  debounce((key, evt) => {
    evt.stopPropagation();
    const value = evt.target.value;
    websocket.sendUpdate([key, "value", value], [key, "changed", true]);
  }, 100)
);

export class ColorPicker extends ShoelaceComponent {
  static eventHandlers() {
    return [onColorChange];
  }
}
