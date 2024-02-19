from .hyperdiv_type import HyperdivType


class CSS(HyperdivType):
    """
    A subclass of @prop_type(HyperdivType) that is used to denote CSS
    props. A prop whose type is a subclass of `CSS` will be rendered
    to CSS in the browser, and used to style the component it is
    attached to, instead of being set as a DOM attribute on that
    component, which is the case for non-`CSS` props.

    For example, @prop_type(CSSField) is a subclass of `CSS`.
    """

    pass
