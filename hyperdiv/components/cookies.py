from datetime import datetime, timezone, timedelta
from ..ui_command import UICommandCache, ui_read, ui_write


class cookies:
    """
    A Hyperdiv interface to browser cookies. Using this interface,
    you can read and write cookies into the user's browser, and this
    data persists across app visits. `cookies` can be used to
    implement authentication and store settings.

    See also: @component(local_storage).

    Like `local_storage`, all methods on `cookies` are static and each
    method call returns an @component(async_command) object. The
    `async_command` value can be used to inspect whether the function
    is still running, and its return value if it is done running.

    Like `local_storage`, `cookies` maintains an internal cache of
    @component(async_command) objects that have been returned by reads
    (`get_cookie`). The cache is keyed by the cookie name. When a
    write (`set_cookie`, `remove_cookie`) is invoked at that key, the
    related `async_command` objects will be cleared. This will trigger
    corresponding reads to re-run and get the new values.

    ## Example

    ```py
    command = hd.cookies.get_cookie("test")

    hd.markdown("`test` value:", command.result)

    if hd.button("Set").clicked:
        hd.cookies.set_cookie("test", "Bunnies")

    if hd.button("Remove").clicked:
        hd.cookies.remove_cookie("test")
    ```

    ## Caveats

    In this implementation of cookies, cookies are read/written solely
    by Javascript in the browser. Therefore the `httpOnly` cookie
    setting is not supported.

    Hyperdiv is currently limited to running at path `/` -- you cannot
    (yet) serve an app from a subpath like `https://foo.com/bar/` --
    and since Hyperdiv serves a single-page app whose routing is
    handled entirely in Javascript, the cookie `path` setting is not
    supported.

    The `expires` setting is also not exposed since it's redundant
    with `max_age`. However, the frontend implementation will set
    `expires` (based on the `max_age` argument) in case an older
    browser doesn't support the `maxAge` setting.

    ## Cookie Expiration

    The `max_age` argument to `set_cookie` allows setting a cookie
    that expires automatically. However, remember that Hyperdiv caches
    cookie reads. In a long running Hyperdiv app, `get_cookie` can
    keep returning an expired cookie value after the browser has
    automatically deleted it.

    To mitigate this, you can periodically re-read the cookie. One
    such pattern:

    ```py-nodemo
    def main():
        s = hd.state(time=time.time())

        cookie_read = hd.cookies.get_cookie("auth_token")
        if cookie_read.done:
            if authenticated(cookie_read.result):
                main_page()
            else:
                login_page()

        if time.time() - s.time > 5:
            cookie_read.clear()
            s.time = time.time()
    ```

    In this pattern, whenever the app runs, it will check if at least
    5 seconds have elapsed since the last read, then it forces a
    re-read by calling `cookie_read.clear()`

    """

    # A cache that remembers results from previous local storage reads
    # (`get_cookie`). When a write is invoked on a key that has been
    # read before, those results are cleared, triggering a re-read.
    _cache = UICommandCache("cookies_result_cache")

    def __init__(self):
        """
        Unlike typical Hyperdiv components, `cookies` cannot be
        instantiated. All methods are static.
        """
        raise Exception("`cookies` cannot be instantiated.")

    @staticmethod
    def get_cookie(name):
        """
        Gets the value of a cookie with the given name. The result
        of the returned @component(async_command) will contain the
        cookie value as a string, or `None` if the cookie does not
        exist.
        """

        if not isinstance(name, str):
            raise ValueError("Cookie names must be strings.")

        result, sent = ui_read("cookies", "getCookie", [name])
        if sent:
            cookies._cache.cache_result(name, result)
        return result

    @staticmethod
    def set_cookie(
        name,
        value,
        expires=None,
        secure=False,
        same_site="lax",
        domain=None,
    ):
        """Sets a cookie

        Args:

        * `name`: The cookie name
        * `value`: The cookie value
        * `expires`: Specifies when the cookie should automatically
          expire. If a positive integer, it is interpreted as the
          lifetime of the cookie in seconds. If a Python `datetime`
          object, it is interpreted as an absolute time in the future
          when the cookie will expire.
        * `domain`: Domain scope (e.g., `".foo.com"`)
        * `secure`: Only send cookie over HTTPS
        * `same_site`: `"strict"`, `"lax"`, or `"none"`

        """

        if not isinstance(name, str):
            raise ValueError("Cookie names must be strings.")

        if not isinstance(value, str):
            raise ValueError("Cookie values must be strings.")

        options = dict()

        if same_site not in ("strict", "lax", "none"):
            raise ValueError("`same_site` must be 'strict', 'lax', or 'none'")

        options["sameSite"] = same_site

        if domain:
            if not isinstance(domain, str):
                raise ValueError("`domain` must be a string.")
            options["domain"] = domain

        if expires:
            expires_dt = None

            if isinstance(expires, int):
                expires_dt = datetime.now(timezone.utc) + timedelta(seconds=expires)
            elif isinstance(expires, datetime):
                expires_dt = expires
                if expires_dt.tzinfo is None:
                    expires_dt = expires_dt.astimezone()
                expires_dt = expires.astimezone(timezone.utc)
            else:
                raise ValueError("`expires` must be an int or a datetime object")

            options["expires"] = expires_dt.isoformat().replace("+00:00", "Z")

        if secure is not None:
            if not isinstance(secure, bool):
                raise ValueError("`secure` must be a bool")

            options["secure"] = secure

        result = ui_write("cookies", "setCookie", [name, value, options])

        cookies._cache.clear_cache_at_key(name)

        return result

    @staticmethod
    def remove_cookie(name):
        """
        Removes a cookie.
        """
        if not isinstance(name, str):
            raise ValueError("Cookie names must be strings.")

        result = ui_write("cookies", "removeCookie", [name])

        cookies._cache.clear_cache_at_key(name)

        return result
