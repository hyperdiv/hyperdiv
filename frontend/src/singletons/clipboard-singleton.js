import { websocket } from "../websocket.js";

class ClipboardSingleton {
  /* eslint-disable class-methods-use-this */
  setComponent(hdNode) {
    if (hdNode.props.value) {
      navigator.clipboard.writeText(hdNode.props.value);
    }
    websocket.sendUpdate(["clipboard", "_value", "$reset"]);
  }

  /* eslint-disable class-methods-use-this */
  getInitialUpdates() {
    return [["clipboard", "_value", ""]];
  }
}

export const clipboardSingleton = new ClipboardSingleton();
