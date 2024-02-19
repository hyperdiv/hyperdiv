let callbacks = [];

export function onNextUpdate(cb) {
  callbacks.push(cb);
}

export function applyPendingCallbacks() {
  setTimeout(() => {
    for (const callback of callbacks) {
      callback();
    }
    callbacks = [];
  });
}
