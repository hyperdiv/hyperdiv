import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onExpand = new EventHandler("sl-expand", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate([key, "expanded", true], [key, "changed", true]);
});

const onCollapse = new EventHandler("sl-collapse", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate([key, "expanded", false], [key, "changed", true]);
});

export class TreeItem extends ShoelaceComponent {
  static eventHandlers() {
    return [onExpand, onCollapse];
  }
}
