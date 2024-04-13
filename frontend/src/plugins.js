import { websocket } from "./websocket.js";

let pluginRegistry = {};
let pluginScriptCache = {};

window.hyperdiv = {
  registerPlugin: (name, callback) => {
    if (name in pluginRegistry) {
      throw new Error(`Duplicate plugin name: ${name}`);
    }
    pluginRegistry[name] = callback;
  },
};

const loadScript = (scriptType, script) => {
  if (script in pluginScriptCache) {
    return pluginScriptCache[script].promise;
  }
  const element = document.createElement("script");
  const promise = new Promise((resolve) => {
    if (scriptType === "js-link") {
      element.src = script;
      element.onload = () => {
        resolve();
      };
    } else if (scriptType === "js") {
      const body = document.createTextNode(script);
      element.appendChild(body);
      resolve();
    }
    document.head.appendChild(element);
  });
  pluginScriptCache[script] = {
    promise,
    element,
  };
  return promise;
};

class PluginContext {
  constructor(key, domElement, initialProps, assetsRoot) {
    this.key = key;
    this.domElement = domElement;
    this.initialProps = initialProps;
    this.assetsRoot = assetsRoot;
    this.updateCallback = () => {};
  }

  updateProp(propName, propValue) {
    websocket.sendUpdate([this.key, propName, propValue]);
  }

  resetProp(propName) {
    websocket.sendUpdate([this.key, propName, "$reset"]);
  }

  onPropUpdate(cb) {
    this.updateCallback = cb;
  }
}

class Plugin extends HTMLElement {
  constructor() {
    super();
    this.component = null;
    this.connected = false;
    this.initialProps = {};
    this.attachShadow({ mode: "open" });
    this.pluginContext = null;
  }

  async connectedCallback() {
    const pluginName = this.component.name;

    const scriptPromises = [];

    for (const [assetType, asset] of this.component.assets) {
      if (assetType === "js" || assetType === "js-link") {
        scriptPromises.push(loadScript(assetType, asset));
      }
    }

    await Promise.all(scriptPromises);

    this.connected = true;

    this.pluginContext = new PluginContext(
      this.getAttribute("id"),
      this.shadowRoot,
      this.initialProps,
      this.component.assetsRoot
    );

    pluginRegistry[pluginName](this.pluginContext);

    this.initialProps = {};
  }

  setComponent(component) {
    this.component = component;

    for (const [assetType, asset] of component.assets) {
      if (assetType === "css-link") {
        const linkElement = document.createElement("link");
        linkElement.rel = "stylesheet";
        linkElement.href = asset;
        this.shadowRoot.appendChild(linkElement);
      } else if (assetType === "css") {
        const styleElement = document.createElement("style");
        styleElement.innerText = asset;
        this.shadowRoot.appendChild(styleElement);
      }
    }
  }

  setProp(propName, propValue) {
    if (!this.connected) {
      this.initialProps[propName] = propValue;
    } else {
      this.pluginContext.updateCallback(propName, propValue);
    }
  }
}

customElements.define("hyperdiv-plugin", Plugin);

export const clearPluginCache = () => {
  pluginRegistry = {};
  for (const script of Object.values(pluginScriptCache)) {
    script.element.remove();
  }
  pluginScriptCache = {};
};
