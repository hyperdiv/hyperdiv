import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { HtmlComponent } from "./core.js";

const onPlay = new EventHandler("play", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate([key, "playing", true]);
});

const onPause = new EventHandler("pause", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate([key, "playing", false]);
});

export class Audio extends HtmlComponent {
  static eventHandlers() {
    return [onPlay, onPause];
  }

  static updateProp(elem, name, propName, propValue) {
    if (propName === "playing") {
      if (propValue) {
        elem.play();
      } else {
        elem.pause();
      }
    } else {
      elem[propName] = propValue;
    }
  }
}
