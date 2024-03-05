import { websocket } from "../websocket.js";
import EventBus from "../event-bus.js";

// https://stackoverflow.com/a/57795495/1417856
const getTheme = () => {
  if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    return "dark";
  }
  return "light";
};

// https://stackoverflow.com/a/57795495/1417856
const themeListener = (cb) => {
  if (window.matchMedia) {
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", (event) => {
        cb(event.matches ? "dark" : "light");
      });
  }
};

class ThemeSingleton extends EventBus {
  constructor() {
    super();
    this.props = { mode: "system", systemMode: getTheme() };
    const userMode = window.localStorage.getItem("$hyperdiv.theme_mode");
    if (userMode === "light" || userMode === "dark") {
      this.props.mode = userMode;
    }
    this.updateClass(this.getCurrentMode());
  }

  getCurrentMode() {
    if (this.props.mode === "system") {
      // If `mode` is system, we follow the browser's system
      // mode. Otherwise we use the user-set `mode`.
      return this.props.systemMode;
    }
    return this.props.mode;
  }

  updateClass(theme) {
    if (theme === this.currentTheme) {
      return;
    }
    const themeClass = `sl-theme-${theme}`;
    document.documentElement.className = themeClass;
    this.currentTheme = theme;

    this.dispatch("theme-change", theme);
  }

  setComponent(hdNode) {
    this.props = hdNode.props;

    this.updateClass(this.getCurrentMode());

    websocket.sendUpdate(["theme", "changed", true]);
  }

  setSystemMode(systemMode) {
    this.props.systemMode = systemMode;
    if (this.props.mode === "system") {
      this.updateClass(systemMode);
    }
  }

  getUpdates() {
    return [
      ["theme", "mode", this.props.mode],
      ["theme", "system_mode", this.props.systemMode],
    ];
  }

  getInitialUpdates() {
    return this.getUpdates();
  }
}

export const themeSingleton = new ThemeSingleton();

themeListener((systemMode) => {
  // Update the theme on the frontend immediately.
  themeSingleton.setSystemMode(systemMode);
  // Send the update to the backend.
  websocket.sendUpdate(...themeSingleton.getUpdates(), [
    "theme",
    "changed",
    true,
  ]);
});
