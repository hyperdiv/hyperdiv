import EventBus from "../event-bus.js";
import { websocket } from "../websocket.js";
import {
  saveScrollPositionsForLocation,
  restoreScrollPositionsForLocation,
} from "../scroll-positions.js";
import { onNextUpdate } from "../next-update.js";

class LocationSingleton extends EventBus {
  constructor() {
    super();

    this.location = this._getLocation();
    this.previousLocation = null;

    if (this.location.hashArg) {
      onNextUpdate(() => this.scrollToHash());
    }

    window.onpopstate = () => {
      const newLocation = this._getLocation();

      if (this._updateLocation(newLocation)) {
        if (this.previousLocation) {
          const previousLocationString = this._getLocationString(
            this.previousLocation
          );
          saveScrollPositionsForLocation(previousLocationString);
          this.previousLocation = newLocation;
        }

        const restoreCallback = () => {
          const locationString = this.getString();
          restoreScrollPositionsForLocation(locationString);
        };
        restoreCallback();
        onNextUpdate(restoreCallback);

        this.dispatch("location-update", newLocation);
      }
    };
  }

  get() {
    return this.location;
  }

  getString() {
    return this._getLocationString(this.location);
  }

  setComponent(hdNode) {
    this.setInternal(hdNode.props, false);
    // setComponent is called when a location update arrives from
    // Python, after the DOM has been updated. In that case we scroll
    // to the hash, if any, immediately.
    if (this.location.hashArg) {
      this.scrollToHash();
    }
  }

  set(location) {
    this.setInternal(location, true);
    // set is called from JS when users click a link. In that case we
    // attempt to scroll to the hash directly. If that does not
    // succeed, because the anchor element was not found, we attempt
    // to scroll again on the next update. This is because when users
    // click a link, it may be either (a) a link to an existing hash
    // on the current page, or (b) a link to to a new page that Python
    // has not yet rendered.
    if (this.location.hashArg) {
      const scrolled = this.scrollToHash();
      if (!scrolled) {
        onNextUpdate(() => this.scrollToHash());
      }
    }
  }

  setInternal(location, dispatch) {
    if (this._updateLocation(location)) {
      if (location.path !== "/" && location.path.endsWith("/")) {
        location.path = location.path.replace(/\/$/, "");
      }
      const locationString = this._getLocationString(location);

      try {
        window.history.pushState(null, "", locationString);
      } catch (e) {
        console.error(`Invalid location: "${locationString}"`);
        return;
      }

      if (dispatch) {
        this.dispatch("location-update", location);
      }
      if (this.previousLocation) {
        const previousLocationString = this._getLocationString(
          this.previousLocation
        );
        saveScrollPositionsForLocation(previousLocationString);
      }
      this.previousLocation = this.location;
    }
  }

  scrollToHash() {
    const location = this.location;

    if (!this.location.hashArg) {
      return false;
    }

    let element = document.getElementById(location.hashArg);
    if (!element) {
      const elements = document.getElementsByName(location.hashArg);
      if (elements.length > 0) {
        element = elements[0];
      }
    }
    if (element) {
      element.scrollIntoView();
      return true;
    }

    return false;
  }

  parseLocation(locationObj) {
    const path = locationObj.pathname;
    let queryArgs = locationObj.search;
    let hashArg = locationObj.hash;
    // get rid of '?'
    if (queryArgs) {
      queryArgs = queryArgs.slice(1);
    }
    // get rid of '#'
    if (hashArg) {
      hashArg = hashArg.slice(1);
    }
    return {
      path,
      queryArgs,
      hashArg,
    };
  }

  // private:

  _updateLocation(newLocation) {
    const oldLocation = this.location;
    if (
      newLocation.path !== oldLocation.path ||
      newLocation.queryArgs !== oldLocation.queryArgs ||
      newLocation.hashArg !== oldLocation.hashArg
    ) {
      this.location = newLocation;
      return true;
    }
    return false;
  }

  _getLocation() {
    const location = this.parseLocation(window.location);
    if (location.path !== "/" && location.path.endsWith("/")) {
      location.path = location.path.replace(/\/$/, "");
      window.history.replaceState(null, "", this._getLocationString(location));
    }
    return location;
  }

  _getLocationString(location) {
    let str = location.path;
    if (location.queryArgs) {
      str += `?${location.queryArgs}`;
    }
    if (location.hashArg) {
      str += `#${location.hashArg}`;
    }
    return str;
  }

  getUpdates(location) {
    return [
      ["location", "path", location.path],
      ["location", "query_args", location.queryArgs],
      ["location", "hash_arg", location.hashArg],
    ];
  }

  getInitialUpdates() {
    const updates = this.getUpdates(this.location);
    return [
      ["location", "protocol", window.location.protocol],
      ["location", "host", window.location.host],
      ...updates,
    ];
  }
}

export const locationSingleton = new LocationSingleton();

locationSingleton.on("location-update", (locationObj) => {
  // When the location bar updates, send the update to the backend.
  websocket.sendUpdate(...locationSingleton.getUpdates(locationObj));
});
