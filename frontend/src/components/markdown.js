import { HtmlComponent } from "./core.js";
import { linkClickHandler } from "./link.js";

// Adds a special click event handler for <a> links, that takes into
// account Hyperdiv routing. Markdown links with external or /assets
// paths will be opened in a new tab, and this behavior cannot
// currently be controlled.
const addLinkClickHandlers = (elem) => {
  const links = elem.getElementsByTagName("a");
  for (const link of links) {
    link.addEventListener("click", (evt) => linkClickHandler(evt, true));
  }
};

// Adds the clipboard button in the top-right of code blocks.
const addClipboardButtons = (elem) => {
  const copyText = "Copy Code";
  const copiedText = "Copied!";

  const codeDivs = elem.querySelectorAll(".codehilite");

  for (const codeDiv of codeDivs) {
    let copyDiv = codeDiv.querySelector(".copybutton");

    if (!copyDiv) {
      copyDiv = document.createElement("div");

      const tooltip = document.createElement("sl-tooltip");
      tooltip.content = copyText;
      tooltip.placement = "top";
      tooltip.hoist = true;

      tooltip.addEventListener("sl-show", (evt) => {
        evt.stopPropagation();
      });
      tooltip.addEventListener("sl-hide", (evt) => {
        evt.stopPropagation();
      });

      const copyButton = document.createElement("sl-icon");
      copyButton.name = "clipboard";

      tooltip.appendChild(copyButton);

      copyDiv.appendChild(tooltip);
      copyDiv.classList.add("copybutton");

      codeDiv.appendChild(copyDiv);

      copyButton.addEventListener("click", () => {
        const toCopy = codeDiv.innerText;

        navigator.clipboard.writeText(toCopy);
        tooltip.content = copiedText;
        setTimeout(() => (tooltip.content = copyText), 1000);
      });
    }
  }
};

export class Markdown extends HtmlComponent {
  static updateProp(elem, name, propName, propValue) {
    if (propName === "content") {
      elem.innerHTML = propValue;
      addClipboardButtons(elem);
      addLinkClickHandlers(elem);
      elem.querySelectorAll("pre").forEach((pre) => {
        if (pre.querySelector("code")) {
          pre.classList.add("has-code");
        }
      });
    } else {
      super.updateProp(elem, name, propName, propValue);
    }
  }
}
