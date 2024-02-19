import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onMenuSelect = new EventHandler("sl-select", (key, evt) => {
  evt.stopPropagation();
  const item = evt.detail.item;
  const updates = [[key, "_selected_item_key", item.id]];
  if (item.type === "checkbox") {
    updates.push([item.id, "checked", item.checked]);
  }
  websocket.sendUpdate(...updates);
});

export class Menu extends ShoelaceComponent {
  static eventHandlers() {
    return [onMenuSelect];
  }
}
