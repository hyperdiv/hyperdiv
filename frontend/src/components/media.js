import debounce from "debounce";
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

const onVolumeChange = new EventHandler(
  "volumechange",
  debounce((key, evt) => {
    evt.stopPropagation();
    websocket.sendUpdate(
      [key, "volume", evt.target.volume],
      [key, "muted", evt.target.muted]
    );
  }, 50)
);

export class Audio extends HtmlComponent {
  static eventHandlers() {
    return [onPlay, onPause, onVolumeChange];
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

export class Video extends Audio {
  static updateProp(elem, name, propName, propValue) {
    if (propName === "width" || propName === "height") {
      if (propValue !== null) {
        elem.setAttribute(propName, propValue);
      }
    } else {
      super.updateProp(elem, name, propName, propValue);
    }
  }
}
