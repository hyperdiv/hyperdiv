class Collector:
    """
    The base class that collects the children of Hyperdiv components
    that can have children.

    Should not be instantiated directly.
    """

    def __init__(self):
        self._children = []

    def _collect_child(self, child):
        self._children.append(child)

    def _extend(self, other_collector):
        for child in other_collector._children:
            self._collect_child(child)


class ShadowCollector(Collector):
    pass


class CollectorStack:
    """Collects the UI hierarchy from the application. The 'stack' handles
    nested containers.

    with box() as b1:   # pushes b1's default slot onto the stack
      text('a')         # collects into b1
      with box() as b2: # pushes b2's default slot onto the stack
        text('b')       # collects into b2
                        # b2 is popped
      text('c')         # collects into b1
                        # b1 is popped

    The top-level of the application is collected into a hidden 'root
    container'.
    """

    def __init__(self):
        self.stack = []

    def push(self, collector):
        self.stack.append(collector)

    def pop(self):
        self.stack.pop()

    def current(self):
        """`current()` is a semi-public interface and can be used by
        components to introspect the parent component in which they're
        being collected. It skips ShadowCollectors which are internal
        collectors used by the cache.
        """
        top_index = -1
        while isinstance(self.stack[top_index], ShadowCollector):
            top_index -= 1
        return self.stack[top_index]

    def internal_current(self):
        return self.stack[-1]

    def collect(self, item):
        self.internal_current()._collect_child(item)
