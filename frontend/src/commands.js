import { websocket } from "./websocket.js";

const commandDefinitions = {
  localStorage: {
    getItem: (args) => localStorage.getItem(...args),
    hasItem: (args) => localStorage.hasOwnProperty(...args),
    setItem: (args) => localStorage.setItem(...args),
    removeItem: (args) => localStorage.removeItem(...args),
    clear: (args) => localStorage.clear(...args),
  },
  cookies: {
    getCookie: (args) => {
      const [name] = args;
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) {
        return parts.pop().split(";").shift();
      }
      return null;
    },
    setCookie: (args) => {
      const [name, value, options] = args;
      let cookieString = `${name}=${value}`;

      // Handle max_age with fallback to expires for old browsers
      if (options.max_age !== null && options.max_age !== undefined) {
        cookieString += `; max-age=${options.max_age}`;

        // Add expires as fallback for ancient browsers (IE < 8)
        // Modern browsers will ignore this since max-age is set
        const expires = new Date();
        expires.setTime(expires.getTime() + options.max_age * 1000);
        cookieString += `; expires=${expires.toUTCString()}`;
      }

      // Always set path=/
      cookieString += "; path=/";

      if (options.domain) {
        cookieString += `; domain=${options.domain}`;
      }
      if (options.secure) {
        cookieString += "; secure";
      }
      if (options.same_site) {
        cookieString += `; samesite=${options.same_site}`;
      }
      document.cookie = cookieString;
      return true;
    },
    removeCookie: (args) => {
      const [name] = args;
      document.cookie = `${name}=; max-age=0; path=/`;
      return true;
    },
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
      [resultKey, "result", result],
    );
  }
};
