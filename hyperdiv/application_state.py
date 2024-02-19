import threading
from .prop import StoredProp


class ApplicationState:
    """Holds persistent prop state."""

    def __init__(self):
        self.state = dict()
        self.state_lock = threading.RLock()

    def _update(self, key, prop_name, value):
        with self.state_lock:
            return self.state[key][prop_name].update(value)

    def _reset(self, key, prop_name):
        with self.state_lock:
            prop = self.state[key][prop_name]
            return prop.reset()

    def _get(self, key, prop_name):
        with self.state_lock:
            return self.state[key][prop_name].value

    def get_props(self, key):
        with self.state_lock:
            return self.state[key]

    def get_prop(self, key, prop_name):
        with self.state_lock:
            return self.state[key][prop_name]

    def has_prop(self, key, prop_name):
        with self.state_lock:
            return prop_name in self.state.get(key, {})

    def init_props(self, key, props_with_values):
        with self.state_lock:
            if key not in self.state:
                self.state[key] = dict()

            for prop, init_value in props_with_values:
                stored_prop = self.state[key].get(prop.name)
                if not stored_prop:
                    stored_prop = StoredProp.create(key, prop)
                    self.state[key][prop.name] = stored_prop
                stored_prop.init(init_value)
            return self.state[key]
