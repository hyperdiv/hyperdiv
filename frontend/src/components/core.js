import {
  onChange,
  onShow,
  onHide,
  onClick,
  onClickPropagate,
  onInput,
} from "./common-handlers.js";

export class HtmlComponent {
  static eventHandlers() {
    return [];
  }

  static create(hdNode) {
    return document.createElement(hdNode.tag);
  }

  static updateProp(elem, name, propName, propValue) {
    elem.setAttribute(propName, propValue);
  }

  static specialSetup() {}
}

export class Plugin extends HtmlComponent {
  static create(hdNode) {
    const elem = super.create(hdNode);
    elem.setComponent(hdNode);
    return elem;
  }

  static updateProp(elem, name, propName, propValue) {
    elem.setProp(propName, propValue);
  }
}

export class ShoelaceComponent extends HtmlComponent {
  static updateProp(elem, name, propName, propValue) {
    elem[propName] = propValue;
  }
}

export class Select extends ShoelaceComponent {
  static eventHandlers() {
    return [onChange, onShow, onHide];
  }

  static specialSetup(elem, hdNode) {
    // Shoelace issue: `select(open=True)` does not render an open
    // select. You have to set it to open manually.
    // https://github.com/shoelace-style/shoelace/issues/1409
    if (hdNode.props.open) {
      setTimeout(() => (elem.open = true));
    }
  }
}

export class Text extends HtmlComponent {
  static updateProp(elem, name, propName, propValue) {
    if (propName === "content") {
      elem.innerHTML = propValue;
    } else {
      super.updateProp(elem, name, propName, propValue);
    }
  }
}

export class Plaintext extends HtmlComponent {
  static create() {
    return document.createTextNode("");
  }
  static updateProp(elem, name, propName, propValue) {
    if (propName !== "content") {
      console.error("Unknown prop on text element", propName);
      return;
    }
    elem.nodeValue = propValue;
  }
}

export class Alert extends ShoelaceComponent {
  static eventHandlers() {
    return [onShow, onHide];
  }
}

export class Avatar extends ShoelaceComponent {
  static eventHandlers() {
    return [onClick];
  }
}

export class Badge extends ShoelaceComponent {
  static eventHandlers() {
    return [onClick];
  }
}

export class Button extends ShoelaceComponent {
  static eventHandlers() {
    return [onClick];
  }
}

export class Details extends ShoelaceComponent {
  static eventHandlers() {
    return [onShow, onHide];
  }
}

export class Dialog extends ShoelaceComponent {
  static eventHandlers() {
    return [onShow, onHide];
  }
}

export class Dropdown extends ShoelaceComponent {
  static eventHandlers() {
    return [onShow, onHide];
  }
}

export class Tooltip extends ShoelaceComponent {
  static eventHandlers() {
    return [onShow, onHide];
  }
}

export class Drawer extends ShoelaceComponent {
  static eventHandlers() {
    return [onHide];
  }
}

export class MenuItem extends ShoelaceComponent {
  static eventHandlers() {
    return [onClickPropagate];
  }
}

export class IconButton extends ShoelaceComponent {
  static eventHandlers() {
    return [onClick];
  }
}

export class RadioGroup extends ShoelaceComponent {
  static eventHandlers() {
    return [onChange];
  }
}

export class TextInput extends ShoelaceComponent {
  static eventHandlers() {
    return [onInput];
  }
}

export class Textarea extends ShoelaceComponent {
  static eventHandlers() {
    return [onInput];
  }
}

export class Slider extends ShoelaceComponent {
  static eventHandlers() {
    return [onInput];
  }
}
