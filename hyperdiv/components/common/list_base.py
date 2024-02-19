from ...component_base import Component
from ...component_mixins.styled import Styled
from ..list_item import list_item


class list_base(Component, Styled):
    """
    Base class for list components.
    """

    def _collect_child(self, child):
        if not isinstance(child, list_item):
            raise Exception("Lists can only contain `list_item` children.")
        super()._collect_child(child)
