from ..prop_types import String, Bool, OneOf, Union, PureString, List, Int, BoolEvent
from ..prop import Prop
from ..slot import Slot
from ..component_mixins.togglable import Togglable
from .common.shoelace_types import ShoelaceSize
from ..style_part import BasePart, StylePart
from .common.label_component import LabelComponent
from .common.text_utils import concat_text
from .text import text
from .option import option
from .icon import icon
from .scope import scope


class select(LabelComponent, Togglable):
    """
    An input component that allows selecting one or more options from
    a dropdown-style menu. Options within a `select` are created using
    @component(option). @component(divider) can be used to insert
    visual separation between option groups.

    ### Single select

    ```py
    with hd.box(gap=1):
        with hd.select(
            placeholder="Choose One:"
        ) as select:
            hd.option("One")
            hd.option("Two")
            hd.divider()
            hd.option("Three")
            hd.option("Four")
        hd.text("Selected:", select.value)
    ```

    ### Multi-select

    When setting `multiple` to `True`, multiple items can be selected,
    and the `value` prop outputs a list of all the selected values.

    ```py
    with hd.box(gap=1):
        with hd.select(
            placeholder="Choose Multiple:",
            value=("One", "Two"),
            multiple=True,
        ) as select:
            hd.option("One")
            hd.option("Two")
            hd.divider()
            hd.option("Three")
            hd.option("Four")
        hd.text("Selected:", select.value)
    ```

    """

    _tag = "sl-select"

    # The name of the select. Relevant when using select in a
    # @component(form). Automatically set to the select's label if
    # `name` is not specified.
    name = Prop(String, "")
    # The value of the select.
    value = Prop(Union(PureString, List(String)), "")
    # The size of the select.
    size = Prop(ShoelaceSize, "medium")
    # Ghost text to render in the select box when no items are
    # selected.
    placeholder = Prop(String, "")
    # Whether this select is exclusive-choice or multiple choice.
    multiple = Prop(Bool, False)
    # The max number of options to render in the select when
    # `multiple` is `True`.
    max_options_visible = Prop(Int, 3)
    # Whether this select can be interacted with.
    disabled = Prop(Bool, False)
    # Renders a clear button that allows clearing all the options in
    # one click.
    clearable = Prop(Bool, False)
    hoist = Prop(Bool, False)
    # Whether to render a filled-background select instead of an outline.
    filled = Prop(Bool, False)
    # Whether to render the select as a pill.
    pill = Prop(Bool, False)
    # Where to open the menu.
    placement = Prop(OneOf("top", "bottom"), "bottom")
    # A small text hint to render under the select.
    help_text = Prop(String, "")
    changed = Prop(BoolEvent, False)

    label_slot = Slot(ui_name="label")
    prefix = Slot()
    clear_icon_slot = Slot(ui_name="clear-icon")
    expand_icon_slot = Slot(ui_name="expand-icon")

    base_style = Prop(BasePart("form-control"))
    label_style = Prop(StylePart("form-control-label"))
    help_text_style = Prop(StylePart("form-control-help-text"))
    input_wrapper_style = Prop(StylePart("form-control-input"))
    combobox_style = Prop(StylePart("combobox"))
    prefix_style = Prop(StylePart("prefix"))
    display_input_style = Prop(StylePart("display-input"))
    listbox_style = Prop(StylePart("listbox"))
    tags_style = Prop(StylePart("tags"))
    tag_style = Prop(StylePart("tag"))
    tag_base_style = Prop(StylePart("tag__base"))
    tag_content_style = Prop(StylePart("tag__content"))
    tag_remove_button_style = Prop(StylePart("tag__remove-button"))
    tag_remove_button_base_style = Prop(StylePart("tag__remove-button__base"))
    clear_button_style = Prop(StylePart("clear-button"))
    expand_icon_style = Prop(StylePart("expand-icon"))

    def __init__(
        self,
        *label,
        options=None,
        name=None,
        prefix_icon=None,
        clear_icon=None,
        expand_icon=None,
        **kwargs,
    ):
        """
        If `options` is given as an iterable of option labels,
        @component(option) components will be automatically created
        for each given option.
        """
        if name is None:
            name = concat_text(label)

        super().__init__(*label, name=name, **kwargs)

        with self:
            if options:
                for o in options:
                    with scope(o):
                        option(o, value=o.replace(" ", "_"))
            if prefix_icon:
                icon(prefix_icon, slot=self.prefix)
            if clear_icon:
                icon(clear_icon, slot=self.clear_icon_slot)
            if expand_icon:
                icon(expand_icon, slot=self.expand_icon_slot)

    def reset(self):
        self.reset_prop("value")

    def _get_label_slot(self):
        return self.label_slot
