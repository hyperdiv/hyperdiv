import Plotly from "plotly.js-dist";
import { themeSingleton } from "../singletons/theme-singleton.js";
import { HtmlComponent } from "./core.js";

export class PlotlyChart extends HtmlComponent {
  static eventHandlers() {
    return [];
  }

  static create(hdNode) {
    console.log(hdNode);
    const elem = super.create(hdNode);
    elem.hdConfig = {
      data: hdNode.props.fig.data,
      layout: hdNode.props.fig.layout,
      browserConfig: hdNode.props.browserConfig,
    };
    Plotly.newPlot(
      elem,
      elem.hdConfig.data,
      elem.hdConfig.layout,
      elem.hdConfig.browserConfig
    ).then(() => {
      window.dispatchEvent(new Event("resize"));
    });
    return elem;
  }

  static updateProp(elem, name, propName, propValue) {
    if (propName === "fig") {
      elem.hdConfig.data = propValue.data;
      elem.hdConfig.layout = propValue.layout;
      Plotly.newPlot(
        elem,
        elem.hdConfig.data,
        elem.hdConfig.layout,
        elem.hdConfig.browserConfig
      );
    } else if (propName === "browserConfig") {
      elem.hdConfig.browserConfig = propValue;
      Plotly.newPlot(
        elem,
        elem.hdConfig.data,
        elem.hdConfig.layout,
        elem.hdConfig.browserConfig
      );
    }
  }
}
