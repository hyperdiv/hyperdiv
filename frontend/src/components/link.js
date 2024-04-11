import { EventHandler } from "./common-handlers.js";
import { websocket } from "../websocket.js";
import { locationSingleton } from "../singletons/location-singleton.js";
import { HtmlComponent } from "./core.js";

export const linkClickHandler = (evt, forceNewTab = false) => {
  let url = null;
  try {
    url = new URL(evt.currentTarget.href);
  } catch (e) {}

  if (!url) {
    // Some components like `breadcrumb_item` don't resolve their
    // `href` prop into a full URL. Instead they send their href prop
    // values verbatim, like `"foo/bar&baz=1"`. In that case we create a
    // temporary <a> node and use it to get a fully resolved URL.

    const node = document.createElement("a");
    node.href = evt.currentTarget.href;
    url = new URL(node.href);
  }

  // If it's an external or assets link:
  if (
    url.host !== window.location.host ||
    url.protocol !== window.location.protocol ||
    url.pathname.startsWith("/assets")
  ) {
    if (forceNewTab) {
      // `forceNewTab` is set to true for links within markdown. In
      // that case we open the link in a new tab.
      evt.preventDefault();
      window.open(url, "_blank").focus();
    }
    // If `forceNewTab` is false, we allow the default action to
    // proceed, which may or may not open the link in a new tab,
    // depending on its "target" attribute.
    return;
  }

  // Otherwise it must be link to a local app path.
  const newLocation = locationSingleton.parseLocation(url);

  const currentLocation = locationSingleton.get();

  if (!newLocation.path) {
    // If the link doesn't specify a path, we leave the current
    // path unchanged
    newLocation.path = currentLocation.path;
    if (!newLocation.queryArgs) {
      // If it also doesn't specify a query param, we leave the
      // current query param unchanged.
      newLocation.queryArgs = currentLocation.queryArgs;
    }
  } else if (!newLocation.path.startsWith("/")) {
    // Handle relative paths by appending the relative path to the
    // existing path.
    let newPath = currentLocation.path;
    if (!newPath.endsWith("/")) {
      newPath += "/";
    }
    newPath += newLocation.path;
    newLocation.path = newPath;
  }

  // Update the location.
  evt.preventDefault();
  locationSingleton.set(newLocation);
};

export const onLinkClick = new EventHandler("click", (key, evt) => {
  linkClickHandler(evt);
});

const onClickDefault = new EventHandler("click", (key, evt) => {
  evt.stopPropagation();
  websocket.sendUpdate([key, "clicked", true]);
});

export class Link extends HtmlComponent {
  static eventHandlers() {
    return [onClickDefault, onLinkClick];
  }
}
