import parse
from functools import wraps
import hyperdiv as hd
from ..frame import Frame


class router:
    """
    Router is useful when building apps with multiple pages. You
    define each page as a function, decorated with its location path,
    and the router will render the right page based on the browser's
    location path.

    ### Basic Use

    The router must be instantiated outside the app, at the global
    level, and app routes are defined using `router.route(path)` as a
    decorator:

    ```py-nodemo
    import hyperdiv as hd

    router = hd.router()

    @router.route("/")
    def home():
       ...

    @router.route("/users")
    def users():
       ...

    def main():
        router.run()

    hd.run(main)
    ```

    `router.run()` will call the correct page function based on the
    browser's @component(location) path. If the browser's path is
    `"/users"`, it will call `users()`. If the path is `"/"`, it will
    call `home()`.

    If the path is an unspecified route, a built-in "not found" page
    is rendered. This page can be customized.

    ### Route Parameters

    Router supports route parameters using
    [parse](https://pypi.org/project/parse/) syntax.

    ```py-nodemo
    @router("/users/{user_id}")
    def users(user_id):
       ...
    ```

    In this example, if users navigate to "/users/123" in the browser,
    the router will invoke `users("123")`.

    Multiple parameters are supported:

    ```py-nodemo
    @router("/org/{org_id}/users/{user_id}")
    def user(org_id, user_id):
       ...
    ```

    In this case, if users navigate to "/org/123/users/456", the
    router will call `users("123", "456")`.

    """

    def __init__(self):
        try:
            Frame.current()
            in_frame = True
        except Exception:
            in_frame = False

        if in_frame:
            raise Exception(
                "router() should not be instantiated inside the Hyperdiv app "
                "function. It should be instantiated in the global scope."
            )

        self.routes = dict()
        self.redirects = dict()
        self.not_found_handler = None

    def _add_route(self, path, fn, redirect_from=None):
        self.routes[path] = fn
        if redirect_from:
            for redirect in redirect_from:
                self.redirects[redirect] = path

    def route(self, path, redirect_from=None):
        """The main decorator for defining routes:

        ```py-nodemo
        @router.route("/foo")
        def foo():
            hd.text("The foo page.")
        ```

        `redirect_from` can be a tuple of paths, such that if the user
        navigates to any those paths, they will be redirected to this
        route.

        In this example, if the user navigates to either "/" or
        "/foo", the location will change to "/foo/bar" and route
        `bar()` will be rendered:

        ```py-nodemo
        @router.route("/foo/bar", redirect_from=("/", "/foo"))
        def bar():
            hd.text("The bar page.")
        ```
        """

        def _route(fn):
            @wraps(fn)
            def wrapper(*args):
                return fn(*args)

            wrapper.path = path

            self._add_route(path, wrapper, redirect_from=redirect_from)

            return wrapper

        return _route

    @property
    def not_found(self):
        """
        A decorator for defining a custom "Not Found" page, to be rendered
        when a user navigates to an undefined path.

        ```py-nodemo
        @router.not_found
        def my_custom_not_found_page():
            with hd.box(gap=1):
                hd.markdown("# Not Found")
                hd.text("There is nothing here.")
        ```
        """

        def _route(fn):
            @wraps(fn)
            def wrapper():
                return fn()

            wrapper.path = None
            self.not_found_handler = wrapper

            return wrapper

        return _route

    def render_not_found(self):
        """
        This method can be used to programmatically invoke the `not_found` route.

        ```py-nodemo
        @router("/users/{user_id}")
        def user(user_id):
            u = get_user(user_id)
            if not u:
                router.render_not_found()
            else:
                hd.text(u.name)
        ```
        """
        loc = hd.location()

        if self.not_found_handler:
            self.not_found_handler()
        else:
            with hd.box(gap=1.5):
                hd.markdown("# Not Found")
                hd.markdown(f"Oops, there is no content at `{loc.path}`")

    def run(self):
        """
        Calls the correct route function based on the current
        @component(location) path. If there is no route corresponding
        to the current path, it renders the `not_found` route.
        """
        loc = hd.location()
        fn = self.routes.get(loc.path)

        if fn:
            with hd.scope(loc.path):
                return fn()

        for route, fn in self.routes.items():
            result = parse.parse(route, loc.path)
            if result:
                args = result.named.values()
                with hd.scope(route + ":" + "#".join(str(arg) for arg in args)):
                    return fn(*result.named.values())

        if loc.path in self.redirects:
            loc.path = self.redirects[loc.path]
            return

        self.render_not_found()
