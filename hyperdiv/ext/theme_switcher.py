import hyperdiv as hd


def theme_switcher(icon_font_size="medium"):
    """
    Renders a theme switcher inline icon and dropdown menu. When the
    icon is clicked, the dropdown menu opens with Dark/Light/System
    choices. The icon is a "moon" icon in dark mode and a "sun" icon
    in light mode.

    This menu remembers the user's setting in browser local storage,
    so if a user chooses Light or Dark mode, that setting will stick
    across app visits. If they choose System, the local storage
    setting is forgotten, as "System" is the default.

    ```py
    hd.theme_switcher()
    ```

    `icon_font_size` takes @prop_type(Size) values and can be used to
    control the size of the inline icon.

    ```py
    hd.theme_switcher(icon_font_size="x-small")
    hd.theme_switcher(icon_font_size=3)
    ```
    """

    theme = hd.theme()

    with hd.dropdown() as dropdown:
        b = hd.icon_button(
            "moon" if not theme.is_light else "sun",
            slot=dropdown.trigger,
            font_size=icon_font_size,
            padding=0.5,
        )

        if b.clicked:
            dropdown.opened = not dropdown.opened

        with hd.menu() as menu:
            item = hd.menu_item("Light", prefix_icon="sun", item_type="checkbox")
            item.checked = theme.mode == "light"

            if menu.selected_item == item:
                item.checked = True
                theme.set_and_remember_theme_mode("light")
                dropdown.opened = False

            item = hd.menu_item("Dark", prefix_icon="moon", item_type="checkbox")
            item.checked = theme.mode == "dark"

            if menu.selected_item == item:
                item.checked = True
                theme.set_and_remember_theme_mode("dark")
                dropdown.opened = False

            hd.divider(spacing="x-small")

            item = hd.menu_item("System", item_type="checkbox")
            item.checked = theme.mode == "system"

            if menu.selected_item == item:
                item.checked = True
                theme.reset_and_forget_theme_mode()
                dropdown.opened = False
