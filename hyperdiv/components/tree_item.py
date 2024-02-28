from ..slot import Slot
from ..prop import Prop
from ..prop_types import Bool, BoolEvent
from ..style_part import StylePart, BasePart
from .common.label_component import LabelComponent
from .icon import icon


class tree_item(LabelComponent):
    """
    A node within a @component(tree).

    Individual `tree_item`s can be disabled, and if they have
    sub-nodes, their expanded/collapsed states can be inspected and
    mutated.

    ```py
    with hd.tree() as t:
        hd.tree_item("One", disabled=True)
        with hd.tree_item(
            "Two", expanded=True
        ) as two:
            three = hd.tree_item("Three")
            hd.tree_item("Four")
        hd.tree_item("Five")


    if hd.button("Toggle Two").clicked:
        two.expanded = not two.expanded
    ```

    """

    _tag = "sl-tree-item"

    # Whether the tree node is expanded.
    expanded = Prop(Bool, False)
    # If `True`, the tree node is not selectable.
    disabled = Prop(Bool, False)
    # `True` for one run if the tree's `expanded` state changed.
    changed = Prop(BoolEvent, False)

    expand_icon = Slot()
    collapse_icon = Slot()

    base_style = Prop(BasePart())
    item_style = Prop(StylePart("item"))
    item_disabled_style = Prop(StylePart("item--disabled"))
    item_expanded_style = Prop(StylePart("item--expanded"))
    item_indeterminate_style = Prop(StylePart("item--indeterminate"))
    item_selected_style = Prop(StylePart("item--selected"))
    indentation_style = Prop(StylePart("indentation"))
    expand_button_style = Prop(StylePart("expand-button"))
    label_style = Prop(StylePart("label"))
    children_style = Prop(StylePart("children"))
    checkbox_style = Prop(StylePart("checkbox"))
    checkbox_base_style = Prop(StylePart("checkbox__base"))
    checkbox_control_style = Prop(StylePart("checkbox__control"))
    checkbox_control_checked_style = Prop(StylePart("checkbox__control--checked"))
    checkbox_control_indeterminate_style = Prop(
        StylePart("checkbox__control--indeterminate")
    )
    checkbox_checked_icon_style = Prop(StylePart("checkbox__checked-icon"))
    checkbox_indeterminate_icon_style = Prop(StylePart("checkbox__indeterminate-icon"))
    checkbox_label_style = Prop(StylePart("checkbox__label"))

    def __init__(
        self,
        *label,
        expand_icon_name=None,
        collapse_icon_name=None,
        **kwargs,
    ):
        """
        @component(icon) names can be passed in `expand_icon_name` or
        `collapse_icon_name` to customize the expand and collapse
        icons of this specific three node. The icons will
        automatically placed in their respective slots.

        These icons override icons set in the parent @component(tree).

        `*label` and `**kwargs` are passed to @component(LabelComponent).
        """
        super().__init__(*label, **kwargs)
        if expand_icon_name or collapse_icon_name:
            with self:
                if expand_icon_name:
                    icon(expand_icon_name, slot=self.expand_icon)
                if collapse_icon_name:
                    icon(collapse_icon_name, slot=self.collapse_icon)

    @property
    def was_expanded(self):
        """
        `True` for one run when the node is expanded.

        Works like a @prop_type(BoolEvent) prop.
        """
        return self.changed and self.expanded

    @property
    def was_collapsed(self):
        """
        `True` for one run when the node is expanded.

        Works like a @prop_type(BoolEvent) prop.
        """
        return self.changed and not self.expanded
