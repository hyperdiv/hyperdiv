import debounce from "debounce";
import { websocket } from "../websocket.js";

class WindowSingleton {
  getUpdates() {
    return [
      ["window", "width", window.innerWidth],
      ["window", "height", window.innerHeight],
    ];
  }

  getInitialUpdates() {
    return this.getUpdates();
  }

  setComponent() {}
}

export const windowSingleton = new WindowSingleton();

window.addEventListener(
  "resize",
  debounce(
    () =>
      websocket.sendUpdate(...windowSingleton.getUpdates(), [
        "window",
        "changed",
        true,
      ]),
    50
  )
);
