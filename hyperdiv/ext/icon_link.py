from ..components.link import link
from ..components.tooltip import tooltip
from ..components.window import window
from ..components.icon import icon
from ..components.text import text


class icon_link(link):
    """
    Renders a @component(link) with a prefix icon. Used mainly in
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

    _name = "link"

    def __init__(
        self,
        icon_name,
        name,
        href,
        responsive_threshold=650,
        font_size="small",
        font_color="neutral-700",
        border_radius="medium",
        hover_background_color="neutral-100",
        direction="horizontal",
        align="center",
        gap=0.5,
        height=2,
        padding=(0.5, 0.7, 0.5, 0.7),
        **kwargs
    ):
        """
        Parameters:

        * `icon_name`: The icon to render in the link.
        * `name`: The rendered name of the link.
        * `href`: The linked URL or path.
        * `responsive_threshold`: The window width, in pixels, below
          which the link name is rendered in a tooltip, instead of
          being rendered inline.

        The rest of the keyword arguments are passed up to
        @component(link).
        """
        w = window()
        show_name = w.width > responsive_threshold

        super().__init__(
            href=href,
            font_size=font_size,
            font_color=font_color,
            border_radius=border_radius,
            hover_background_color=hover_background_color,
            direction=direction,
            align=align,
            gap=gap,
            height=height,
            padding=padding,
            collect=False,
            **kwargs
        )

        with self:
            icon(icon_name)
            if show_name:
                text(name)

        if show_name:
            self.collect()
        else:
            with tooltip(name):
                self.collect()
