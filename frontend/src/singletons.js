import { themeSingleton } from "./singletons/theme-singleton.js";
import { locationSingleton } from "./singletons/location-singleton.js";
import { clipboardSingleton } from "./singletons/clipboard-singleton.js";
import { windowSingleton } from "./singletons/window-singleton.js";

export const singletons = {
  location: locationSingleton,
  theme: themeSingleton,
  clipboard: clipboardSingleton,
  window: windowSingleton,
};

export const getInitialUpdates = () => {
  const initialUpdates = [];

  for (const singleton of Object.values(singletons)) {
    initialUpdates.push(...singleton.getInitialUpdates());
  }

  return initialUpdates;
};
