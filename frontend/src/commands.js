import { websocket } from "./websocket.js";

const commandDefinitions = {
  localStorage: {
    getItem: (args) => localStorage.getItem(...args),
    hasItem: (args) => localStorage.hasOwnProperty(...args),
    setItem: (args) => localStorage.setItem(...args),
    removeItem: (args) => localStorage.removeItem(...args),
    clear: (args) => localStorage.clear(...args),
  },
};

export const executeCommands = (commands) => {
  for (const { resultKey, target, command, args } of commands) {
    const targetCommands = commandDefinitions[target];
    if (typeof targetCommands !== "object") {
      console.error(`Could not find target ${target}`);
      return;
    }
    const commandDefinition = targetCommands[command];
    if (typeof commandDefinition !== "function") {
      console.error(`Could not find command ${target}.${command}`);
      return;
    }

    const result = commandDefinition(args);
    websocket.sendUpdate(
      [resultKey, "running", false],
      [resultKey, "done", true],
      [resultKey, "result", result]
    );
  }
};
