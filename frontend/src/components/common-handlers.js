import debounce from "debounce";
import { websocket } from "../websocket.js";

export class EventHandler {
  constructor(eventName, handler) {
    this.eventName = eventName;
    this.handler = handler;
  }
}

export const onClick = new EventHandler("click", (key, evt) => {
  evt.stopPropagation();
  evt.preventDefault();
  websocket.sendUpdate([key, "clicked", true]);
});

export const onClickPropagate = new EventHandler("click", (key, evt) => {
  evt.preventDefault();
  websocket.sendUpdate([key, "clicked", true]);
});

export const onShow = new EventHandler("sl-show", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate(
    [key, "opened", true],
    [key, "visibility_changed", true]
  );
});

export const onHide = new EventHandler("sl-hide", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate(
    [key, "opened", false],
    [key, "visibility_changed", true]
  );
});

export const onInput = new EventHandler(
  "sl-input",
  debounce((key, evt) => {
    evt.stopPropagation();
    websocket.sendUpdate(
      [key, "value", evt.target.value],
      [key, "changed", true]
    );
  }, 200)
);

export const onChange = new EventHandler("sl-change", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate(
    [key, "value", evt.target.value],
    [key, "changed", true]
  );
});
