from .. import design_tokens as tokens
from .hyperdiv_type import HyperdivType


class DesignToken(HyperdivType):
    """
    `DesignToken(design_token_enum)` creates a Hyperdiv type that
    accepts any value of the given design token enum.
    """

    def __init__(self, enum):
        if not issubclass(enum, tokens.TokenEnum):
            raise ValueError(f"DesignToken got non-token enum: {enum}")

        self.enum = enum
        self.elems = set([e for e in list(enum)])
        self.values = set([e.value for e in list(enum)])
        self.value_to_elem = {e.value: e for e in self.elems}

    def parse(self, value):
        if value in self.values:
            return value
        if value in self.elems:
            return value.value
        raise ValueError(f"Unexpected value {value} for enum type {self.enum}.")

    def render(self, value):
        return self.value_to_elem[value].render()

    def __repr__(self):
        return f"DesignToken[{self.enum}]"
