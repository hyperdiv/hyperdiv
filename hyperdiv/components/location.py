from ..prop_types import HyperdivType, PureString, String, Optional
from ..prop import Prop
from ..ui_singleton import BrowserSingleton


def check_forbidden_delimiters(value):
    if "#" in value:
        raise ValueError("'#' cannot occur in a path")
    if "?" in value:
        raise ValueError("'?' cannot occur in a path")


class LocationPartDef(HyperdivType):
    """
    This type is used by @component(location) to express location
    parts. It takes a string but it rejects strings containing the
    characters `"?"` or `"#"`.
    """

    def parse(self, value):
        path = String.parse(value)
        check_forbidden_delimiters(path)
        return value

    def render(self, path):
        return String.render(path)

    def __repr__(self):
        return "LocationPart"


LocationPart = LocationPartDef()


class PathStringDef(LocationPartDef):
    """
    This type is used by @component(location) to express the location path.
    It takes a string but:

    * It rejects path strings containing the characters `"?"` or `"#"`.
    * If the path string is "/", it leaves it as is.
    * If the path string is empty, it sets it to "/".
    * If the path ends in "/", it strips the trailing "/". So
      "/foo/bar/" is set to "/foo/bar"
    """

    def parse(self, value):
        path = super().parse(value)
        if path == "":
            path = "/"
        if path != "/":
            path = path.rstrip("/")
        return path

    def __repr__(self):
        return "PathString"


PathString = PathStringDef()


class location(BrowserSingleton):
    """
    `location` is a Hyperdiv component that gives access to the
    browser's location bar.  Using `location`, you can render
    different things for different location paths, query args, and
    hash args.

    `location` offers three props: `path`, `query_args`, and `hash_arg`.

    If the browser location is `https://my-app.com/foo/bar?a=1&b=2#hello`, then:

    * `location().protocol == "https:"`
    * `location().host == "my-app.com"`
    * `location().path == "/foo/bar"`
    * `location().query_args == "a=1&b=2"`
    * `location().hash_arg == "hello"`

    You can change the location by using the `go()` method. For
    example, to change the location to `"/foo/bar"`, you can call
    `location().go(path="/foo/bar")`.

    Changing the location by using `go()` or mutating the location
    props is useful in some cases, but in general is an anti-pattern
    and you should instead use @component(link)s to implement
    navigation.
    """

    _key = "location"

    # The protocol part of the browser location bar.
    protocol = Prop(Optional(PureString), backend_immutable=True)
    # The host part of the browser location bar.
    host = Prop(Optional(PureString), backend_immutable=True)
    # The path part of the browser location bar.
    path = Prop(Optional(PathString))
    # The query args part of the browser location bar, not including
    # the leading `?`.
    query_args = Prop(Optional(LocationPart))
    # The hash part of the location bar, not including the leading
    # `#`.
    hash_arg = Prop(Optional(LocationPart))

    def go(self, path, query_args="", hash_arg=""):
        """
        Change the browser location bar by simultaneously mutating all
        three props. For example, `go(path="/foo", hash_arg="bar")` will
        set the location to `"/foo#bar"`. If `query_args` is currently
        set to a value, if will be set to `""`.

        If you need to programmatically mutate the location, this is
        the recommended way to do it. If instead you mutate
        individual props, say `location().path = "/foo"`, that will
        only change the path prop, and let the other props remain
        unchanged, which is probably not what you want.
        """
        self.path = path
        self.query_args = query_args
        self.hash_arg = hash_arg

    def to_string(self):
        """
        Returns a string of the full location, suitable for pasting into
        the browser's location bar.
        """
        string = f"{self.protocol}//{self.host}{self.path}"
        if self.query_args:
            string += f"?{self.query_args}"
        if self.hash_arg:
            string += f"#{self.hash_arg}"
        return string
