from .common.label_component import LabelComponent


class list_item(LabelComponent):
    """
    A list item component to be used with @component(list) or @component(ordered_list).
    Not useful on its own.
    """

    _tag = "li"
