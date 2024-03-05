import debounce from "debounce";
import { websocket } from "../websocket.js";
import { HtmlComponent } from "./core.js";
import { EventHandler } from "./common-handlers.js";

const onSubmit = new EventHandler("submit", (key, evt) => {
  evt.preventDefault();
  debounce((key, evt) => {
    const isValid = evt.target.reportValidity();
    if (isValid) {
      websocket.sendUpdate([key, "_submit_clicked", true]);
    }
  }, 200)(key, evt);
});

export class Form extends HtmlComponent {
  static eventHandlers() {
    return [onSubmit];
  }
}
