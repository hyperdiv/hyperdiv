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
    this.set(hdNode.props);
  }

  set(location, dispatch = false) {
    if (this._updateLocation(location)) {
      const locationString = this._getLocationString(location);

      try {
        window.history.pushState(
          // Push the scroll position into the state, too, to be
          // restored when this state is popped.
          // { scroll: scrollPosition },
          null,
          "",
          locationString
        );
      } catch (e) {
        console.error(`Invalid location: "${locationString}"`);
        return;
      }

      // saveScrollPositionsForLocation(locationString);

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
    this.scrollToHash();
  }

  scrollToHash() {
    const location = this.location;
    if (location.hashArg) {
      let element = document.getElementById(location.hashArg);
      if (!element) {
        const elements = document.getElementsByName(location.hashArg);
        if (elements.length > 0) {
          element = elements[0];
        }
      }
      if (element) {
        element.scrollIntoView();
      }
    }
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
    return this.parseLocation(window.location);
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
