import "@shoelace-style/shoelace/dist/themes/light.css";
import "@shoelace-style/shoelace/dist/themes/dark.css";
import "./styles/fonts.css";
import "./styles/syntax.css";
import "./styles/overrides.css";
import "./shoelace.js";
import "./disconnected-cover";
import { websocket } from "./websocket.js";
import { updateStyle, removeStyles, removeAllStyles } from "./css.js";
import { singletons, getInitialUpdates } from "./singletons.js";
import { applyPendingCallbacks } from "./next-update.js";
import { executeCommands } from "./commands.js";
import { clearPluginCache } from "./plugins.js";
import { locationSingleton } from "./singletons/location-singleton.js";
import {
  getScrollPositions,
  restoreScrollPositionsForLocation,
} from "./scroll-positions.js";
import { getComponentLogic } from "./components.js";

let elementCache = {};

// Creates an HTML node from the given Hyperdiv node
// `hdNode`. Populates the given node cache `cache` and style cache
// `styleCache` with the HTML node and its styles.
const createDomNode = (hdNode, cache, styleCache) => {
  const { key, name, tag, props, children, classes, style } = hdNode;

  const component = getComponentLogic(name, tag);

  // Create the HTML node and set its ID

  const elem = component.create(hdNode);
  elem.id = key;

  // Add CSS classes

  for (const className of classes) {
    elem.classList.add(className);
  }

  // Set props and children

  for (const propName of Object.keys(props)) {
    component.updateProp(elem, name, propName, props[propName]);
  }

  if (children) {
    for (const child of children) {
      const domNode = createDomNode(child, cache, styleCache);
      elem.appendChild(domNode);
    }
  }

  // Install event handlers

  const eventHandlers = component.eventHandlers();

  for (const eventHandler of eventHandlers) {
    elem.addEventListener(eventHandler.eventName, (event) =>
      eventHandler.handler(key, event)
    );
  }

  // Some components need specific treatment due to idiosyncrasies in
  // Shoelace

  component.specialSetup(elem, hdNode);

  // Populate caches

  styleCache[key] = style;
  cache[key] = { name, tag, element: elem };

  return elem;
};

// Saves the current scroll positions and restores them after the dom
// update is done. This maintains scroll positions after a
// disconnect/reconnect, and in particular helps with development, as
// code edits do not cause the containers to jarringly scroll back to
// the top.
function saveAndRestoreScrollPositions() {
  // Save the current scroll positions.
  const scrollPositions = getScrollPositions();
  // Restore the scroll positions after the dom update is done.
  setTimeout(() => {
    restoreScrollPositionsForLocation(
      locationSingleton.getString(),
      scrollPositions
    );
  });
}

// Updates the global element cache and style cache with the given
// cache objects.
const updateCaches = (cache, styleCache) => {
  // Repopulate the element cache.
  for (const key in cache) {
    if (Object.prototype.hasOwnProperty.call(cache, key)) {
      elementCache[key] = cache[key];
    }
  }

  // Repopulate the style cache.
  for (const key in styleCache) {
    if (Object.prototype.hasOwnProperty.call(styleCache, key)) {
      updateStyle(key, styleCache[key]);
    }
  }
};

// Replaces the DOM body with a new DOM that is created from the given
// Hyperdiv dom structure.
const setRootDom = (dom) => {
  // First, clear the existing element cache, plugin cache, and style
  // cache.
  clearPluginCache();
  elementCache = {};
  removeAllStyles();

  // Create the root dom node, which will populate the `cache` and
  // `styleCache` with cache entries.
  const cache = {};
  const styleCache = {};

  const rootNode = createDomNode(dom, cache, styleCache);

  // Update the global caches
  updateCaches(cache, styleCache);

  // Saves the current scroll positions and restores them after a timeout,
  // after the dom has been updated with the new root.
  saveAndRestoreScrollPositions();

  // Empty out the body
  document.body.innerHTML = "";
  // Add the new root node to the body
  document.body.appendChild(rootNode);
};

// Removes removed nodes from the cache.
const clearCache = (nodes) => {
  const traverse = (node) => {
    if (node.id && node.id in elementCache) {
      delete elementCache[node.id];
    }
    if (node.childNodes && node.childNodes.length) {
      for (const child of node.childNodes) {
        traverse(child);
      }
    }
  };

  for (const node of nodes) {
    traverse(node);
  }
};

// Removes styles for removed nodes.
const clearStyles = (nodes) => {
  const traverse = (node) => {
    if (node.id) {
      removeStyles([node.id]);
    }
    if (node.childNodes && node.childNodes.length) {
      for (const child of node.childNodes) {
        traverse(child);
      }
    }
  };
  for (const node of nodes) {
    traverse(node);
  }
};

// Applies an incoming diff to the DOM.
const applyDiff = (diff) => {
  const cache = {};
  const styleCache = {};

  for (const key of Object.keys(diff)) {
    const propDiff = diff[key].props;
    const childrenDiff = diff[key].children;
    const styleDiff = diff[key].style;
    const { element, name, tag } = elementCache[key];

    // Update changed props
    if (propDiff) {
      const component = getComponentLogic(name, tag);

      for (const propName of Object.keys(propDiff)) {
        component.updateProp(element, name, propName, propDiff[propName]);
      }
    }

    // Update changed children
    if (childrenDiff) {
      for (const chunk of childrenDiff) {
        const cmd = chunk[0];

        if (cmd === "insert") {
          const startIndex = chunk[1];
          const nodesToInsert = chunk[2];

          if (startIndex === element.childNodes.length) {
            for (const node of nodesToInsert) {
              const dom = createDomNode(node, cache, styleCache);
              element.appendChild(dom);
            }
          } else {
            const sentinelNode = element.childNodes[startIndex];
            for (const node of nodesToInsert) {
              const dom = createDomNode(node, cache, styleCache);
              element.insertBefore(dom, sentinelNode);
            }
          }
        } else if (cmd === "delete") {
          const startIndex = chunk[1];
          let howMany = chunk[2];

          const removedElements = [];

          while (howMany > 0) {
            const toRemove = element.childNodes[startIndex];
            removedElements.push(toRemove);
            toRemove.remove();
            howMany -= 1;
          }

          clearStyles(removedElements);
          clearCache(removedElements);
        }
      }
    }

    // Update the global caches.
    updateCaches(cache, styleCache);

    // Update changed styles.
    if (styleDiff !== undefined) {
      updateStyle(key, styleDiff);
    }
  }
};

// Start the websocket and handle incoming messages.
websocket.setInitialUpdatesCallback(getInitialUpdates);
websocket.start();

websocket.on("message", (message) => {
  if (message.diff) {
    applyDiff(message.diff);
  } else if (message.dom) {
    setRootDom(message.dom);
  }

  if (message.singletons) {
    for (const componentName of Object.keys(message.singletons)) {
      const singleton = singletons[componentName];
      singleton.setComponent(message.singletons[componentName]);
    }
  }

  if (message.commands) {
    setTimeout(() => executeCommands(message.commands));
  }

  applyPendingCallbacks();
});
