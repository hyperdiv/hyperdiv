import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onAnimationFinish = new EventHandler("sl-finish", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate([key, "play", "$reset"]);
});

export class Animation extends ShoelaceComponent {
  static eventHandlers() {
    return [onAnimationFinish];
  }
}
