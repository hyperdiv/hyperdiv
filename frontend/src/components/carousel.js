import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onCarouselSlideChange = new EventHandler(
  "sl-slide-change",
  (key, evt) => {
    evt.stopPropagation();
    const item = evt.detail.slide;
    websocket.sendUpdate([key, "_selected_item_key", item.id]);
  }
);

export class Carousel extends ShoelaceComponent {
  static eventHandlers() {
    return [onCarouselSlideChange];
  }
}
