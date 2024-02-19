import ChartJS from "chart.js/auto";
import "chartjs-adapter-date-fns";
import { themeSingleton } from "../singletons/theme-singleton.js";
import { HtmlComponent } from "./core.js";

/*
 * Colors are passed by the backend as Shoelace CSS variable strings,
 * like "var(--sl-color-blue-400)". This function rewrites these CSS
 * variable strings with actual colors by looking up the values of
 * those variables in the current document. In addition, it adds some
 * opacity to background colors.
 */
function transformColors(data, options) {
  const style = getComputedStyle(document.body);

  const getVarValue = (varName, opacity) => {
    if (!varName.startsWith("var(")) {
      return varName;
    }
    // Grab the variable name out of the `var(...)` string:
    const extracted = varName.match(/var\(([^)]+)\)/)[1];
    // Grab the actual color from the document:
    const color = style.getPropertyValue(extracted);
    // Add opacity by transforming the hsl() value into a hsla() value
    // with an additional opacity component:
    if (opacity && color.startsWith("hsl(")) {
      const colorValues = color.slice(4, -1);
      const joined = colorValues.split(" ").join(", ");
      return `hsla(${joined}, ${opacity})`;
    }
    return color;
  };

  // Rewrite dataset colors:
  for (const dataset of data.datasets) {
    for (const prop of ["borderColor", "backgroundColor"]) {
      if (!dataset[prop]) {
        continue;
      }
      // We store the original Shoelace variable string in a hidden
      // property prefixed by `$`. This is necessary, because on theme
      // change (dark mode <-> light mode), we need to re-access those
      // variable strings.
      const hiddenProp = "$" + prop;
      if (!dataset[hiddenProp]) {
        dataset[hiddenProp] = dataset[prop];
      }
      // Add 0.8 opacity to backgroudn colors.
      let opacity = null;
      if (prop === "backgroundColor") {
        opacity = 0.5;
      }
      // In polar charts, colors come in an array, one for each slice.
      if (dataset[hiddenProp].constructor === Array) {
        dataset[prop] = dataset[hiddenProp].map((c) => getVarValue(c, opacity));
      } else {
        dataset[prop] = getVarValue(dataset[hiddenProp], opacity);
      }
    }
  }

  if (!options.scales) {
    return;
  }

  // Rewrite grid colors:
  for (const axis of ["x", "y", "r"]) {
    if (options.scales[axis]) {
      if (!options.scales[axis].grid.$color) {
        options.scales[axis].grid.$color = options.scales[axis].grid.color;
      }
      options.scales[axis].grid.color = getVarValue(
        options.scales[axis].grid.$color
      );
    }
  }
}

export class Chart extends HtmlComponent {
  static eventHandlers() {
    return [];
  }

  static create(hdNode) {
    const domNode = document.createElement("div");
    domNode.style.overflow = "hidden";

    const canvasNode = document.createElement("canvas");
    domNode.appendChild(canvasNode);

    // Rewrite colors in the initial payload:
    transformColors(hdNode.props.config.data, hdNode.props.config.options);

    const chart = new ChartJS(canvasNode, hdNode.props.config);

    // Rewrite colors on theme change:
    themeSingleton.on("theme-change", () => {
      transformColors(chart.data, chart.options);
      chart.update("none");
    });

    // Attach the chart object to the dom node, to access later, on
    // prop updates.
    domNode.chart = chart;

    return domNode;
  }

  static updateProp(elem, name, propName, propValue) {
    if (propName === "config") {
      transformColors(propValue.data, propValue.options);
      elem.chart.type = propValue.type;
      elem.chart.data = propValue.data;
      elem.chart.options = propValue.options;
      elem.chart.update("none");
    }
  }
}
