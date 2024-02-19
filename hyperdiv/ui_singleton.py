from .component_base import BaseState


class SingletonCollector(type):
    """
    Collects Singleton and BrowserSingleton classes as they are defined. The
    singleton classes have to be instantiated in bulk by `AppRunner`,
    and this class provides the mechanism that collects all the
    singletons in one place.

    BrowserSingletons are singletons that are sent to the browser, like
    `location` and `theme`. Singletons stay on the backend and don't
    have a browser counterpart.
    """

    ui_singleton_classes: set[type] = set()
    singleton_classes: set[type] = set()

    def __new__(cls, clsname, bases, attrs):
        klass = super().__new__(cls, clsname, bases, attrs)
        if clsname not in ("BrowserSingleton", "Singleton"):
            if issubclass(klass, Singleton):
                SingletonCollector.singleton_classes.add(klass)
            elif issubclass(klass, BrowserSingleton):
                SingletonCollector.ui_singleton_classes.add(klass)
        return klass

    @staticmethod
    def create_ui_singletons():
        return [
            component_class()
            for component_class in SingletonCollector.ui_singleton_classes
        ]

    @staticmethod
    def create_singletons():
        return [
            component_class()
            for component_class in SingletonCollector.ui_singleton_classes.union(
                SingletonCollector.singleton_classes
            )
        ]


class BrowserSingleton(BaseState, metaclass=SingletonCollector):
    """
    A browser singleton is a non-UI component that communicates values
    between Python <-> browser.

    All instances of a BrowserSingleton class share the same underlying
    state.
    """

    def __init__(self):
        """BrowserSingleton should not be instantiated directly."""
        super().__init__()


class Singleton(BaseState, metaclass=SingletonCollector):
    """
    A Singleton is a non-UI component that never gets sent to the
    frontend. It is backend-only.

    All instances of a Singleton class share the same underlying
    state.
    """

    def __init__(self):
        """Singleton should not be instantiated directly."""
        super().__init__()
