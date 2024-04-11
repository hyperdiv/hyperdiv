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
  sendUpdate: (key, propName, propValue) => {
    websocket.sendUpdate([key, propName, propValue]);
  },
};

const loadScript = (scriptType, script) => {
  if (script in pluginScriptCache) {
    return pluginScriptCache[script];
  }
  const ret = new Promise((resolve) => {
    const scriptTag = document.createElement("script");
    if (scriptType === "js-link") {
      scriptTag.src = script;
      scriptTag.onload = () => {
        resolve();
      };
    } else if (scriptType === "js") {
      const body = document.createTextNode(script);
      scriptTag.appendChild(body);
      resolve();
    }
    document.head.appendChild(scriptTag);
  });
  pluginScriptCache[script] = ret;
  return ret;
};

class Plugin extends HTMLElement {
  constructor() {
    super();
    this.component = null;
    this.connected = false;
    this.initialProps = {};
    this.updateFunction = null;
    this.attachShadow({ mode: "open" });
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
    this.updateFunction = pluginRegistry[pluginName]({
      key: this.getAttribute("id"),
      domElement: this.shadowRoot,
      initialProps: this.initialProps,
      assetsRoot: this.component.assetsRoot,
    });
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
      this.updateFunction(propName, propValue);
    }
  }
}

customElements.define("hyperdiv-plugin", Plugin);

export const clearPluginCache = () => {
  pluginRegistry = {};
  pluginScriptCache = {};
};
