export default class EventBus {
  constructor() {
    this.events = {};
  }

  on(name, callback) {
    if (!this.events[name]) {
      this.events[name] = [];
    }
    this.events[name].push(callback);
    return callback;
  }

  off(name, callback = null) {
    if (this.events[name]) {
      if (callback) {
        this.events[name] = this.events[name].filter((cb) => cb !== callback);
      }
      if (this.events[name].length === 0 || !callback) {
        delete this.events[name];
      }
    }
  }

  dispatch(name, ...args) {
    if (this.events[name]) {
      this.events[name].forEach((callback) => callback(...args));
    }
  }
}
