import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onSelectionChange = new EventHandler(
  "sl-selection-change",
  (key, evt) => {
    evt.stopPropagation();
    const selectedKeys = evt.detail.selection.map((elem) => elem.id);
    websocket.sendUpdate(
      [key, "_selected_keys", selectedKeys],
      [key, "selection_changed", true]
    );
  }
);

export class Tree extends ShoelaceComponent {
  static eventHandlers() {
    return [onSelectionChange];
  }
}
