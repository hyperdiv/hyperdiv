import hyperdiv as hd
from .theme_switcher import theme_switcher as hyperdiv_theme_switcher
from .navigation_menu import navigation_menu
from .icon_link import icon_link


class template:
    """
    Provides an app template for building apps with a top-bar,
    sidebar, sidebar navigation menu, logo, title, dark mode switcher,
    and top-bar links.

    Typical usage:

    ```py-nodemo
    app = hd.template(title="Hello", logo="/assets/logo.svg")
    app.add_sidebar_menu(my_menu)
    app.add_topbar_links(my_links)
    with app.body:
        my_app_contents()
    ```

    """

    def __init__(
        self,
        logo=None,
        title=None,
        sidebar=True,
        theme_switcher=True,
        responsive_threshold=1000,
        responsive_topbar_links_threshold=600,
    ):
        """
        Parameters:

        * `logo`: The path to a logo image,
          e.g. `/assets/logo.svg`. The logo will be rendered in the
          top-left corner of the app.

        * `title`: The title of the app, rendered in the top-left
          next to the logo.

        * `sidebar`: Whether to render a sidebar.

        * `theme_switcher`: Whether to render the theme/dark-mode
          switcher in the top-right.

        * `responsive_threshold`: The width of the window (in pixels),
          below which the sidebar is rendered as a togglable drawer
          instead of as an in-line sidebar.

        * `responsive_topbar_links_threshold`: The width of the window
          (in pixels) below which the topbar icons are rendered as
          icon+hover tooltip instead of icon+name.
        """

        window = hd.window()
        wide = window.width > responsive_threshold

        self._responsive_topbar_links_threshold = responsive_topbar_links_threshold

        self._drawer = None
        self._drawer_title = None
        self._sidebar = None

        if sidebar:
            self._drawer = hd.drawer(
                width=20,
                background_color="neutral-50",
                body_style=hd.style(padding=0),
                panel_style=hd.style(background_color="neutral-0"),
                title_style=hd.style(padding=(1.5, 1, 1.5, 2)),
            )

            if window.changed and wide:
                self._drawer.opened = False

            with hd.box(collect=False) as self._drawer_title:
                if title:
                    hd.text(title, font_weight="bold")

            self._sidebar = hd.box(
                width=20,
                shrink=False,
                padding=2,
                gap=1,
                horizontal_scroll=True,
                collect=False,
            )

        with hd.box(height="100vh"):
            with hd.box(
                background_color="neutral-50",
                shrink=False,
                padding=(1, 1, 1, 2),
            ) as self._header:
                with hd.hbox(justify="space-between", align="center"):
                    with hd.hbox(gap=1, align="center"):
                        if sidebar and not wide:
                            if hd.icon_button("list").clicked:
                                self._drawer.opened = not self._drawer.opened
                        if logo or title:
                            with hd.link(
                                href="/",
                                direction="horizontal",
                                gap=1,
                                align="center",
                                font_color="neutral-900",
                            ):
                                if logo:
                                    hd.image(logo, height=2)
                                with hd.box() as self._app_title:
                                    if title:
                                        hd.text(title, font_weight="bold")
                    with hd.hbox(align="center"):
                        self._topbar_links = hd.hbox(align="center")
                        if theme_switcher:
                            hyperdiv_theme_switcher()

            with hd.hbox(grow=True, horizontal_scroll=False):
                if sidebar:
                    if wide:
                        self._sidebar.collect()
                    else:
                        with self._drawer:
                            with hd.hbox(
                                gap=1, align="center", slot=self._drawer.label_slot
                            ):
                                if logo:
                                    hd.image(logo, height=2)
                                self._drawer_title.collect()
                            self._sidebar.collect()
                with hd.scope(hd.location().path):
                    self._body = hd.box(
                        padding=2, gap=1, grow=True, horizontal_scroll=True
                    )

    @property
    def sidebar(self):
        """
        The sidebar container, a @component(box).

        If the template was constructed with `sidebar=False`, this
        property evaluates to `None`.
        """
        return self._sidebar

    def add_sidebar_menu(self, link_dict, expanded=False):
        """
        Adds a @component(navigation_menu) to the sidebar. `link_dict` is
        passed to @component(navigation_menu) to construct the menu
        and add it to the sidebar container.

        The template's `drawer` property is passed into the navigation
        menu as its `drawer` kwarg, so the drawer is auto-closed when
        a link is clicked.

        The `expanded` kwarg is passed down to
        @component(navigation_menu), causing the menu sections to stay
        expanded if `True`.

        If the template was constructed with `sidebar=False`, calling
        this function will raise an error.
        """
        if not self._sidebar:
            raise Exception("There is no sidebar.")
        with self._sidebar:
            navigation_menu(link_dict, drawer=self._drawer, expanded=expanded)

    @property
    def topbar_links(self):
        """The topbar links container, a @component(box)."""
        return self._topbar_links

    def add_topbar_link(self, icon, name, href):
        """
        Adds a @component(icon_link) component to the `topbar_links`
        container. The `icon`, `name`, and `href` components are
        passed to the @component(icon_link) constructor.

        The app template's `responsive_topbar_links_threshold` setting
        is passed down as @component(icon_link)'s
        `responsive_threshold` parameter.
        """
        with self._topbar_links:
            icon_link(
                icon,
                name,
                href,
                responsive_threshold=self._responsive_topbar_links_threshold,
            )

    def add_topbar_links(self, link_dict):
        """
        Adds multiple @component(icon_link) components to the
        `topbar_links` container in one shot.

        The `link_dict` syntax is the same as the `linked_dict` passed
        to @component(navigation_menu), but only flat menus are
        supported in this case.
        """
        for link_name, settings in link_dict.items():
            with hd.scope(link_name):
                icon = settings["icon"]
                href = settings["href"]
                self.add_topbar_link(icon, link_name, href)

    @property
    def body(self):
        """
        The app's main container, where the main content is
        rendered. A @component(box).
        """
        return self._body

    @property
    def app_title(self):
        """
        The app's title container, a @component(box).

        This container usually holds the logo and the title, passed to
        the template using the `logo` and `title` kwargs.

        If you want to place custom content in this container, leave
        the `logo` and `title` kwargs blank, and instead place
        components into this container.
        """
        return self._app_title

    @property
    def drawer_title(self):
        """
        The drawer's title container, a @component(box).

        This container plays the same role as the `app_title`
        container, but in the app's drawer instead of on the base page.

        This container usually holds the same exact contents as the
        `app_title` container when you use the `logo` and `title`
        kwargs to construct the template.

        If you want to place custom contents in the drawer title area,
        omit those kwargs and instead place components into this
        container.

        Note that if you place custom components in the `app_title`
        container, those components will not be added to the
        `drawer_title` container.

        If the template was constructed with `sidebar=False`, this
        property evaluates to `None`.
        """
        return self._drawer_title

    @property
    def drawer(self):
        """
        The drawer component, a @component(drawer).

        Normally you shouldn't need to manipulate the drawer, but
        sometimes it may be useful to programmatically set its
        `opened` prop to open/close the drawer.

        If the template was constructed with `sidebar=False`, this
        property evaluates to `None`.
        """
        return self._drawer

    @property
    def header(self):
        """
        The header container, a @component(box).

        This container holds the `app_title` and `topbar_links`
        containers, and the theme switcher.
        """
        return self._header
