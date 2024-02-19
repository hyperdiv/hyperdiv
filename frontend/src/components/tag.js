import { EventHandler, onClick } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { ShoelaceComponent } from "./core.js";

const onTagRemove = new EventHandler("sl-remove", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate([key, "removed", true]);
});

export class Tag extends ShoelaceComponent {
  static eventHandlers() {
    return [onClick, onTagRemove];
  }

  static specialSetup(elem) {
    // Shoelace issue: Clicking the close button on a tag propagates
    // the click to the tag itself.
    setTimeout(() => {
      const removeButton = elem.shadowRoot.querySelector(
        '[part="remove-button"]'
      );
      if (removeButton) {
        removeButton.addEventListener("click", (event) =>
          event.stopPropagation()
        );
      }
    });
  }
}
