from ...component_base import Component
from ...component_mixins.styled import Styled
from ...debug import logger
from ..text import text
from ..plaintext import plaintext
from .text_utils import concat_text


class LabelComponent(Component, Styled):
    """
    A convenience component base class for components that tend to
    contain a text label in their bodies or in a slot. The main
    purpose of this class is to expose a `label` property as a
    convenience to set/get the label.

    The label is assumed to be held in a `plaintext` or `text`
    component.

    Note that if the user explicitly sets the body to something that
    is not a plaintext/text component, the `label` attribute will no
    longer work.
    """

    def __init__(self, *label, **kwargs):
        """
        If `*label` is provided, it will be concatenated by spaces and
        stored as a `text` or `plaintext` component in the component's
        body.

        If `*label` is not provided, it is assumed the caller will
        store the label explicitly.

        `**kwargs` are passed up to @component(Component).
        """
        super().__init__(**kwargs)
        self._label_slot = self._get_label_slot()

        if label:
            with self:
                if self._label_slot:
                    text(concat_text(label), slot=self._label_slot)
                else:
                    plaintext(concat_text(label))

    def _get_label_slot(self):
        """
        Override this to return a slot in which the label is stored, if any.
        """
        return None

    @property
    def label(self):
        """
        Reads/writes the label.

        If the label slot has been manually populated by the user with
        something other than a text or plaintext component, reading
        this property returns `None`, and writing it does nothing.
        """
        item = self._find_plaintext_child(self._label_slot)
        if item:
            return item.content

    @label.setter
    def label(self, value):
        item = self._find_plaintext_child(self._label_slot)
        if item:
            item.content = value

    def _find_plaintext_child(self, slot):
        candidate_child = None
        if not slot:
            if len(self.children) > 0:
                candidate_child = self.children[0]
        else:
            for child in self.children:
                if child.slot == slot:
                    candidate_child = child
                    break

        if isinstance(candidate_child, (text, plaintext)):
            return candidate_child

        logger.warning(f"Could not find a label on {self.__class__}.")

        return None
