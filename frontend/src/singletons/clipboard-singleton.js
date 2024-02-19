import { websocket } from "../websocket.js";

class ClipboardSingleton {
  setComponent(hdNode) {
    if (hdNode.props.value) {
      navigator.clipboard.writeText(hdNode.props.value);
      // reset the value back to null
      websocket.sendUpdate(["clipboard", "_value", null]);
    }
  }

  /* eslint-disable class-methods-use-this */
  getInitialUpdates() {
    return [];
  }
}

export const clipboardSingleton = new ClipboardSingleton();
