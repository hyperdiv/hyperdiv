import debounce from "debounce";
import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onImageComparerChange = new EventHandler(
  "sl-change",
  debounce((key, evt) => {
    evt.stopPropagation();
    websocket.sendUpdate([key, "position", evt.target.position]);
  }, 100)
);

export class ImageComparer extends ShoelaceComponent {
  static eventHandlers() {
    return [onImageComparerChange];
  }
}
