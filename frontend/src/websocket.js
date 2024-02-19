import EventBus from "./event-bus.js";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/* A helper message queue that allows a reader to wait for messages
 * while concurrent writers add messages. When a message is added, the
 * reader is immediately unblocked. Currently it only supports a
 * single reader. */

class PendingMessages {
  constructor() {
    this.messages = [];
    this.resolve = null;
    this.batchTimeout = null;
  }

  /* Can be used to wait for up to `timeout` milliseconds for messages
   * to appear, without using CPU. Only one call at a time is supported. */
  waitForMessages(timeout) {
    return new Promise((resolve) => {
      let waitTimeout;

      this.resolve = () => {
        this.resolve = null;
        clearTimeout(waitTimeout);
        resolve();
      };

      if (this.messages.length > 0) {
        this.resolve();
      } else {
        waitTimeout = setTimeout(this.resolve, timeout);
      }
    });
  }

  /* Empty out and return the contents of the message queue. */
  getMessages() {
    const { messages } = this;
    this.messages = [];
    return messages;
  }

  /* Add a message to the queue. */
  addMessage(message) {
    this.messages.push(message);
    // By delaying the resolve, we give an opportunity for multiple
    // events that are fired near-simultaneously (e.g. a click and
    // location change firing at the same time when clicking a link)
    // to be batched. This helps avoid multiple backend renders to
    // happen sequentially in response to near-simultanous events.
    if (!this.batchTimeout) {
      this.batchTimeout = setTimeout(() => {
        if (this.resolve) {
          this.resolve();
        }
        this.batchTimeout = null;
      });
    }
  }
}

/* The core connection logic for Hyperdiv. Upon calling start(), an
 * infinite loop is launched which maintains a connection and flushes
 * messages to the server. When the connection breaks, the loop
 * actively reconnects. */
class Websocket extends EventBus {
  constructor() {
    super();

    this.pendingMessages = new PendingMessages();
    this.websocket = null;
    this.connected = false;
    this.started = false;
    this.initialUpdatesCallback = () => [];
  }

  setInitialUpdatesCallback(cb) {
    this.initialUpdatesCallback = cb;
  }

  makeWebsocketUrl() {
    const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    let url = `${wsProtocol}//${window.location.host}/ws`;

    const params = [];

    if (this.clientId) {
      params.push(`clientId=${this.clientId}`);
    }

    // Attach "initial updates" as query parameters to the websocket
    // URL. Initial updates are updates from singletons, like theme
    // and location. Instead of connecting, and then sending the
    // browser location and theme system setting, we attach them to
    // the websocket URL to avoid multiple round-trips and a visual
    // flash (e.g. the UI is rendered in light mode, but the user
    // setting is dark mode, so the UI would flash from light to
    // dark).
    const initialUpdates = this.initialUpdatesCallback();

    if (initialUpdates) {
      const encodedUpdates = encodeURIComponent(JSON.stringify(initialUpdates));
      params.push(`updates=${encodedUpdates}`);
    }

    if (params.length > 0) {
      url += "?" + params.join("&");
    }

    return url;
  }

  connect() {
    return new Promise((resolve, reject) => {
      if (this.websocket) {
        // Paranoid preemptive close in case the websocket object is
        // in "open" state while the transport is broken.
        try {
          this.websocket.close();
        } catch (e) {
          // Ignore any errors
        }
      }
      const url = this.makeWebsocketUrl();
      this.websocket = new WebSocket(url);
      this.websocket.addEventListener("open", () => {
        resolve();
      });
      this.websocket.addEventListener("message", (wsMessage) => {
        const message = JSON.parse(wsMessage.data);
        if ("clientId" in message) {
          this.clientId = message.clientId;
        }
        this.dispatch("message", message);
      });
      // TODO: for connections that open successfully, the error event
      // can be used to immediately detect when the connection dies --
      // e.g., it could be used to immediately reject `waitForMessages()`
      this.websocket.addEventListener("error", reject);
    });
  }

  start(initialUpdates) {
    if (this.started) {
      throw new Error("The websocket is already running.");
    }
    this.initialUpdates = initialUpdates;
    this.started = true;
    this.loop();
  }

  /* Infinite connect/send loop. The loop has two inner loops: a
   * connect loop and a send loop. The connect loop retries until a
   * connection is established, and then it breaks out to the send
   * loop. The send loop keeps sending messages to the server until
   * the connection breaks, in which case it breaks back up to the
   * connect loop. */
  async loop() {
    while (true) {
      if (this.connected) {
        this.dispatch("connection-change", false);
      }
      this.connected = false;
      // Connect loop. Keep trying to connect in a loop, waiting a bit
      // in between, until it succeeds.
      while (true) {
        try {
          await this.connect();
          this.connected = true;
          this.dispatch("connection-change", true);
          // If connecting succeeded, break out to the message loop
          // below.
          break;
        } catch (e) {
          await sleep(1000);
          continue;
        }
      }
      // Message sending loop. Keep looping and sending any messages
      // that accumulate in the pending list.
      while (true) {
        // Wait for up to 50ms to get messages to avoid a busy loop
        await this.pendingMessages.waitForMessages(50);

        // If the connection closed, break to the outer loop which
        // will reconnect.
        if (this.websocket.readyState === WebSocket.CLOSED) {
          break;
        }

        // Note: It's still possible that the conection broke
        // immediately after the check above, so it's possible that
        // messages can be lost. The only way to make sure that no
        // messages are lost is to implement retry with server acks.

        // Send all the messages.
        const messages = this.pendingMessages.getMessages();
        if (messages.length > 0) {
          this.websocket.send(JSON.stringify(messages));
        }
      }
    }
  }

  /* Send a message to the server. */
  sendUpdate(...updates) {
    this.pendingMessages.addMessage({
      type: "update",
      updates,
    });
  }
}

export const websocket = new Websocket();
