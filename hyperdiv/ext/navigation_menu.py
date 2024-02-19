import hyperdiv as hd


def get_active_route(links):
    loc = hd.location()

    for link_name, settings in links.items():
        href = settings["href"]

        if href == loc.path:
            return href

    for link_name, settings in links.items():
        href = settings["href"]

        if loc.path.startswith(href + "/"):
            return href


def link_group(links, drawer=None):
    """
    Renders a group of links. This is usually the whole menu, in flat
    menus, or the link group within a menu section, in hierarchical
    menus.

    If an optional `drawer` is passed, the drawer is closed when a
    link is clicked.
    """
    active_route = get_active_route(links)

    with hd.animation(play=True, duration=200):
        with hd.box_list(gap=0.1, vertical_scroll=False):
            for link_name, settings in links.items():
                href = settings["href"]
                icon = settings.get("icon")
                with hd.scope(f"{link_name}:{href}"):
                    with hd.box_list_item():
                        with hd.link(
                            href=href,
                            direction="horizontal",
                            align="center",
                            gap=0.5,
                            font_color="neutral-800",
                            hover_background_color=(
                                "neutral-100" if active_route == href else "neutral-50"
                            ),
                            background_color=(
                                "neutral-100" if active_route == href else None
                            ),
                            border_radius="medium",
                            padding=(0.2, 0.5, 0.2, 0.5),
                        ) as link:
                            if icon:
                                hd.icon(icon)
                            hd.text(link_name)
                        if drawer and link.clicked:
                            drawer.opened = False


def nav_section(name, links, drawer=None, expanded=False):
    """
    Renders a collapsible section, including the section title and
    expand/collapse logic.
    """
    state = hd.state(expanded=expanded)
    active_route = get_active_route(links)

    if active_route:
        state.expanded = True

    with hd.box(gap=0.5):
        with hd.animation(name="shake") as shake_anim:
            header_link = hd.button(
                name,
                variant="text",
                height=1.8,
                label_style=hd.style(
                    padding=(0, 0.5, 0, 0),
                    font_color="neutral-800",
                    font_weight="bold",
                ),
                margin=0,
            )

            with header_link:
                hd.icon(
                    "chevron-down" if state.expanded else "chevron-right",
                    slot=header_link.suffix,
                )

        if not expanded and header_link.clicked:
            if active_route and state.expanded:
                shake_anim.play = True
            else:
                state.expanded = not state.expanded

        if state.expanded:
            link_group(links, drawer=drawer)


def navigation_menu(link_dict, drawer=None, expanded=False):
    """
    Renders a navigation menu component. The menu is wrapped in a
    @component(nav) and uses @component(link) for each link.

    `link_dict` is a dictionary specifying the menu, which can be
    either a flat menu, or a two-level hierarchical menu.

    `drawer` is an optional @component(drawer). If a drawer is passed,
    when a link is clicked, the drawer is automatically closed. This is
    a niche use case for @component(template), where a navigation menu
    is rendered in the sidebar drawer.

    If `expanded` is `True`, the menu sections will render fully
    expanded and are not collapsible.

    ### Flat Menu

    ```py
    hd.navigation_menu({
        "Home": {"href": "/"},
        "Users": {"href": "/users"},
        "Google": {"href": "https://google.com"},
    })
    ```
    `"href"` specifies a path (or external URL) to which Hyperdiv
    navigates when you click the menu item.

    ### Icons

    Navigation menus support optional prefix icons by setting `"icon"`
    in each link to an icon name:

    ```py
    hd.navigation_menu({
        "Home": {"href": "/", "icon": "house"},
        "Users": {"href": "/users", "icon": "people"},
        "Google": {"href": "https://google.com", "icon": "google"},
    })
    ```

    ### Hierarchical Menu

    `link_dict` also supports a syntax for specifying two-level menus
    (Section -> Menu) with collapsible sections, by adding an extra
    level to the `link_dict`:

    ```py
    hd.navigation_menu({
        "Application": {
            "Home": {"href": "/", "icon": "house"},
            "Users": {"href": "/users", "icon": "people"},
        },
        "Resources": {
            "Google": {"href": "https://google.com", "icon": "google"},
            "Facebook": {"href": "https://google.com", "icon": "facebook"},
        }
    })
    ```

    """
    current_group = None

    with hd.nav(gap=1, font_size="small") as menu:
        for key, value in link_dict.items():
            if "href" in value:
                if not current_group:
                    current_group = dict()
                current_group[key] = value
            else:
                if current_group:
                    link_group(current_group, drawer=drawer)
                    current_group = None
                with hd.scope(key):
                    nav_section(key, value, drawer=drawer, expanded=expanded)
        if current_group:
            link_group(current_group, drawer=drawer)

    return menu
