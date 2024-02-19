import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onTabClose = new EventHandler("sl-close", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate([key, "closed_clicked", true]);
});

export class Tab extends ShoelaceComponent {
  static eventHandlers() {
    return [onTabClose];
  }
}
