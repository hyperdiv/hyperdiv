import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onTabShow = new EventHandler("sl-tab-show", (key, evt) => {
  evt.stopPropagation();
  const tabKey = evt.detail.name;
  websocket.sendUpdate([key, "_active_tab_key", tabKey]);
});

export class TabGroup extends ShoelaceComponent {
  static eventHandlers() {
    return [onTabShow];
  }
}
