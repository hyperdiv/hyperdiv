from ..slot import Slot
from ..prop import Prop
from ..prop_types import OneOf, List, PureString, Size, Color, CSSField, BoolEvent
from ..component_mixins import Styled
from ..component_base import Component
from ..style_part import BasePart
from .tree_item import tree_item
from .icon import icon


class tree(Component, Styled):
    """An arbitrarily nested tree component.

    ```py
    with hd.tree(indent_guide_width="1px"):
        hd.tree_item("One")
        hd.tree_item("Two")
        with hd.tree_item("Three"):
            hd.tree_item("Three A")
            hd.tree_item("Three B")
            with hd.tree_item("Three C"):
                hd.tree_item("Three C-1")
                hd.tree_item("Three C-2")
            hd.tree_item("Three D")
        hd.tree_item("Four")
        hd.tree_item("Five")
    ```

    ## Selected Items

    The nodes of the tree can be selected with the mouse or keyboard.
    Selection can be customized to select multiple nodes, a single
    node, or a single leaf.

    You can use the `selected_items` method to get the currently
    selected @component(tree_item) sub-nodes.

    You can also use the `selection_changed` event prop to do
    something when the selection changes.

    ```py
    selection = hd.radio_buttons(
        "single", "multiple", "leaf",
        value="single"
    )

    with hd.tree(
        indent_guide_width="1px",
        selection=selection.value
    ) as tree:
        one = hd.tree_item("One")
        hd.tree_item("Two")
        with hd.tree_item("Three"):
            hd.tree_item("Three A")
            hd.tree_item("Three B")
            with hd.tree_item("Three C"):
                hd.tree_item("Three C-1")
                three_c_2 = hd.tree_item("Three C-2")
            hd.tree_item("Three D")
        hd.tree_item("Four")
        hd.tree_item("Five")

    hd.text("Selected:", [item.label for item in tree.selected_items])

    alert = hd.alert("The selection changed!", duration=1000)

    if tree.selection_changed:
        alert.opened = True

    """

    _tag = "sl-tree"

    # The selection type.
    #
    # * `single`: Only single nodes can be selected, whether they are
    #   leaf nodes or intermediate nodes.
    # * `leaf`: Only leaf nodes can be selected.
    # * `multiple`: Multiple nodes can be selected. When selecting an
    #   intermediate node, its entire subtree is selected.
    selection = Prop(OneOf("single", "multiple", "leaf"), "single")
    # `True` for one run when the selection changes.
    selection_changed = Prop(BoolEvent, False)
    _selected_keys = Prop(List(PureString), ())

    # How far nested children are indented.
    indent_size = Prop(CSSField("--indent-size", Size))
    # The size of the indent guide.
    indent_guide_width = Prop(CSSField("--indent-guide-width", Size))
    # The color of the indent guide.
    indent_guide_color = Prop(CSSField("--indent-guide-color", Color))
    # The vertical offset of the indent guide.
    indent_guide_offset = Prop(CSSField("--indent-guide-offset", Size))
    # The border style of the indent guide.
    indent_guide_style = Prop(
        CSSField("--indent-guide-style", OneOf(None, "dotted", "dashed", "solid"))
    )

    expand_icon = Slot()
    collapse_icon = Slot()

    base_style = Prop(BasePart())

    def __init__(
        self,
        expand_icon_name=None,
        collapse_icon_name=None,
        **kwargs,
    ):
        """
        @component(icon) names can be passed in `expand_icon_name` or
        `collapse_icon_name` to customize the expand and collapse
        icons of all expandable tree nodes. The icons will
        automatically placed in their respective slots.

        The rest of `**kwargs` are passed to `Component`.
        """
        super().__init__(**kwargs)
        if expand_icon_name or collapse_icon_name:
            with self:
                if expand_icon_name:
                    icon(expand_icon_name, slot=self.expand_icon)
                if collapse_icon_name:
                    icon(collapse_icon_name, slot=self.collapse_icon)

    @property
    def selected_items(self):
        """
        Returns the complete list of the @component(tree_item) children
        that are currently selected.
        """

        children = []

        def collect_children(node):
            for c in node.children:
                if isinstance(c, tree_item):
                    if c._key in self._selected_keys:
                        children.append(c)
                    collect_children(c)

        collect_children(self)
        return children
