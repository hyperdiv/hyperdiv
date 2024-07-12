import debounce from "debounce";
import { websocket } from "../websocket.js";
import { HtmlComponent } from "./core.js";
import { EventHandler } from "./common-handlers.js";

/*
 Workaround to avoid showing the focus outline when clicking on the
 file uploader component, but to show it when tabbing into it with the
 keyboard.
 */
export const onClick = new EventHandler("click", (key, evt) => {
  const tag = evt.target.tagName;
  const type = evt.target.getAttribute("type");

  if (
    tag === "INPUT" &&
    type === "file" &&
    // https://stackoverflow.com/questions/61323376/how-to-know-that-a-onclick-event-is-called-from-mouseclick-or-pressing-the-enter
    !(evt.screenX === 0 || evt.screenY === 0)
  ) {
    evt.target.blur();
  }
});

export class FileInput extends HtmlComponent {
  static eventHandlers() {
    return [onClick];
  }

  // static create(hdNode) {
  //   const container = document.createElement("label");
  //   const input = document.createElement("input");
  //   input.setAttribute("type", "file");
  //   container.appendChild(input);
  //   container.classList.add("file-upload");
  //   return container;
  // }
}
