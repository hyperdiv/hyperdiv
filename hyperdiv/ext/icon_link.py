import hyperdiv as hd


def icon_link(icon, name, href, responsive_threshold=650):
    """Renders a @component(link) with a prefix icon. Used mainly in
    @component(template) to add top-bar links to a template.

    ```py
    hd.icon_link(
        "book",
        "Documentation",
        "https://docs.foo.com"
    )
    ```

    If the window is narrower than `responsive_threshold` pixels, the
    icon link is rendered as an icon only, and its name is rendered in
    a hover tooltip:

    ```py
    hd.icon_link(
        "book",
        "Documentation",
        "https://docs.foo.com",
        responsive_threshold=10000
    )
    ```
    """
    w = hd.window()

    def link(show_name=True):
        with hd.link(
            href=href,
            font_size="small",
            font_color="neutral-700",
            border_radius="medium",
            hover_background_color="neutral-100",
        ):
            with hd.hbox(
                align="center",
                gap=0.5,
                height=2,
                padding=(0.5, 0.7, 0.5, 0.7),
            ):
                hd.icon(icon)
                if show_name:
                    hd.text(name)

    if w.width < responsive_threshold:
        with hd.tooltip(name):
            link(show_name=False)
    else:
        link(show_name=True)
