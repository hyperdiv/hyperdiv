import asyncio
from ..prop_types import Bool, BoolEvent, PureString
from ..prop import Prop
from ..debug import logger
from .common.text_utils import concat_text
from .box import box
from .text import text
from .button import button
from .switch import switch
from .checkbox import checkbox
from .state import state
from .slider import slider
from .select_ import select
from .color_picker import color_picker
from .text_input import text_input
from .textarea import textarea
from .radio_group import radio_group
from .task import task


def required_validation(value):
    if not value:
        return "You must provide a value."
    else:
        return None


def no_validation(value):
    return None


class FormControlWrapper:
    """
    Manages a form input component and its validation. It wraps a box
    around the component, and places the validation error message
    under the component.

    The wrapper box can be customized with style/box kwargs provided
    in `wrapper_style`.
    """

    def __init__(self, wrapper_style=None, validation=None, is_async=False):
        self.validation = validation or no_validation
        self.is_async = is_async
        kwargs = wrapper_style.props_as_dict() if wrapper_style else dict()
        gap = kwargs.pop("gap", None) or 0.1
        self.box = box(gap=gap, **kwargs)
        self.state = state(error_message=None)
        self.task = task()

    def __enter__(self):
        self.box.__enter__()
        return self.box

    def __exit__(self, exc_type, exc_val, exc_tb):
        error = (
            self.task.done and self.task.result
            if self.is_async
            else self.state.error_message
        )
        if error:
            text(error, font_color="red-600", font_size="small")
        self.box.__exit__(exc_type, exc_val, exc_tb)

    def form_control(self):
        return self.box.children[0]

    def validate(self):
        form_control = self.form_control()
        if self.is_async:
            self.task.rerun(self.validation, form_control.value)
        else:
            self.state.error_message = self.validation(form_control.value)

    def is_valid(self):
        if self.is_async:
            return self.task.done and not self.task.result
        return self.state.error_message is None

    def is_pending(self):
        return self.is_async and self.task.running

    def get_name_value(self):
        form_control = self.box.children[0]
        return form_control.name, form_control.value

    def reset(self):
        self.state.error_message = None
        self.task.clear()
        form_control = self.box.children[0]
        form_control.reset()


class form(box):
    """
    This is the core component for creating Hyperdiv forms with
    validation.

    `form` inherits from @component(box) and accepts the same props
    for laying out its children. A form can contain arbitrary
    components in addition to the form's inputs.

    `form` provides methods for adding input components such as
    @component(button), @component(checkbox), @component(select),
    etc. Input components should be added to the form using these
    methods. Otherwise, the form will not be aware of those components
    being part of the form. Using these methods, the user can set up
    validation for each component by passing `required=True`, which
    uses a basic built-in validation, or passing a custom validation
    function using the `validation` kwarg.

    When the form is submitted, by either clicking the submit button
    or pressing Enter while an input is focused, validation is run on
    all the form inputs. If validation fails on an input component,
    the validation error message is rendered next to that component.

    A validation function inputs the component's value and returns
    `None` if validation is successful, or an error message if the
    validation failed. The error message is bubbled up to the user.

    If the form was submitted and validation passed, the `submitted`
    attribute of the form becomes `True`, and the `form_data` property
    can be used to access the input components' values in the form of
    a dictionary mapping input names to input values.

    ```py
    with hd.form() as form:
        form.text_input(
            "Enter some text",
            required=True
        )
        form.submit_button()
    if form.submitted:
        print(form.form_data)
    ```

    In the example above, if you leave the text input empty and submit
    the form, a validation error message will be rendered. If you
    input some text and press Enter, the form data dictionary will be
    printed at the command line.

    ### Custom validation

    In this example, the form will not pass validation unless the word
    `"bunny"` is typed in the text input:

    ```py
    def bunny_validation(value):
        if value != "bunny":
            return "Please enter 'bunny'"

    with hd.form() as form:
        form.text_input(
            "Enter some text",
            validation=bunny_validation
        )
        form.submit_button()
    if form.submitted:
        print(form.form_data)
    ```

    Since validation is implemented with Python functions, arbitrarily
    complex validation can be expressed. Here is an email validator using
    the Python package [email-validator](https://pypi.org/project/email-validator/):

    ```py
    def validate_email(email):
        import email_validator

        try:
            email_validator.validate_email(email)
        except Exception as e:
            return str(e)

    with hd.form() as form:
        form.text_input(
            "Enter your email",
            validation=validate_email,
        )
        form.submit_button()
    if form.submitted:
        print(form.form_data)
    ```

    ### Async validation

    If validation function calls are heavy, they can be made async and
    they will run in the background, keeping the UI responsive.

    If a validation function is defined with `async def`, it will
    automatically be run in the background. If a validation function
    is not defined with `async_def`, it can be made to run in the
    background by passing it to the form control using the
    `async_validation` keyword argument instead of `validation`.

    ```py
    async def bunny_validation(value):
        import asyncio
        await asyncio.sleep(1)
        if value != "bunny":
            return "Please enter 'bunny'"

    with hd.form() as form:
        form.text_input(
            "Enter some text",
            validation=bunny_validation
        )
        form.submit_button()
    if form.submitted:
        print(form.form_data)
    ```

    ### Names and values

    The form data dictionary returned by `form_data` can be curated by
    providing custom names to the input components. By default their
    labels are used as names, but custom names will override that
    behavior.

    ```py
    with hd.form() as form:
        form.text_input(
            "Enter some text",
            name="text"
        )
        form.checkbox(
            "Include Shipping",
            name="shipping"
        )
        form.submit_button()
    if form.submitted:
        print(form.form_data)
    ```

    The `form.form_data` dictionary will look like `{'text': 'Some
    text', 'shipping': True}`.

    ### Resetting a form

    `form` provides the `reset_button` method which will add a reset
    button to the form, that when clicked will reset all the form's
    inputs to to initial values.

    ```py
    with hd.form() as form:
        form.text_input(
            "Enter some text",
            name="text"
        )
        form.checkbox(
            "Include Shipping",
            name="shipping",
            checked=True
        )
        with hd.hbox(gap=1):
            form.submit_button()
            form.reset_button()
    if form.submitted:
        print(form.form_data)
    ```

    """

    _tag = "form"

    # Disable frontend validation, since Hyperdiv forms are validated
    # in Python.
    _novalidate = Prop(PureString, "", ui_name="novalidate")

    # When users click the submit button.
    _submit_clicked = Prop(BoolEvent, False)
    # Triggered internally when a form has async validations and all
    # the validations have finished running, and the form is valid.
    _async_resubmitted = Prop(BoolEvent, False)
    # When the user clicks submit, this becomes True, and is reset
    # when the form finishes validating.
    _being_submitted = Prop(Bool, False, internal=True)

    def __init__(self, disabled=False, gap=1, **kwargs):
        """
        If `disabled` is `True`, all the form inputs will be rendered
        disabled, overriding the individual `disabled` kwargs passed
        to each input. If you mutated the `disabled` prop on any of
        the form inputs, that mutated value will take precedence.

        The rest of the kwargs are passed to the `box` superclass.
        """
        super().__init__(gap=gap, **kwargs)

        self.disabled = disabled
        self.form_controls = []
        self.is_valid = True
        self.names = set()

        if self._submit_clicked:
            self._being_submitted = True

    @property
    def submitted(self):
        """
        Returns `True` if the form was submitted and all fields passed
        validation, and `False` otherwise.

        This property acts like an event, and becomes `True` once per
        submission.
        """
        submitted = self._submit_clicked
        submitted = self._async_resubmitted or submitted
        return submitted and self.is_valid

    @property
    def being_submitted(self):
        """
        Returns `True` if a submit request is currently being processed,
        and `False` otherwise.
        """
        return self._being_submitted

    @property
    def submit_failed(self):
        """
        Returns `True` if the form was submitted and some of the
        validations failed.

        Returns `False` if the form was submitted and all the
        validations passed.

        Returns `None` if the form is pending submission. This will
        happen when some of the fields use async validation.
        """
        if self._async_resubmitted:
            return not self.is_valid
        elif self._submit_clicked:
            if self._being_submitted:
                return None
            else:
                return not self.is_valid
        return None

    @property
    def form_data(self):
        """
        When `submitted` is `True`, this property returns a dictionary
        mapping form field names to values. If `submitted` is not `True`,
        this property returns `None`.

        If the user has not provided a value for the `name` prop on
        any field in the form, that field's label will be used
        instead.

        ```py
        with hd.form() as form:
            form.text_input("An input")
            form.text_input("Another input", name="another-input")

        if form.submitted:
            # prints {'An input': '', 'another-input', ''}
            print(form.form_data)
        ```

        """
        if not self.submitted:
            return None
        data = dict()
        for fc in self.form_controls:
            name, value = fc.get_name_value()
            data[name] = value
        return data

    def _form_control(
        self,
        control_fn,
        *label,
        has_label=True,
        validation=None,
        async_validation=None,
        required=None,
        wrapper_style=None,
        **kwargs,
    ):
        is_async = False

        if validation and async_validation:
            raise Exception(
                "The `validation` and `async_validation` args cannot be set simultaneously."
            )

        if validation and asyncio.iscoroutinefunction(validation):
            is_async = True
        elif async_validation:
            validation = async_validation
            is_async = True

        if required and not validation:
            validation = required_validation

        if validation and required is None:
            required = True

        fc = FormControlWrapper(
            validation=validation, is_async=is_async, wrapper_style=wrapper_style
        )
        self.form_controls.append(fc)

        name = kwargs.pop("name", None)
        if not name:
            name = concat_text(label)
        if not name:
            raise Exception(f"Form elements must have a name or label.")
        if name in self.names:
            raise Exception(f"Name collision on name: '{name}'")
        self.names.add(name)

        if required and label:
            label = label + (" *",)

        with fc:
            disabled = (
                self.disabled or kwargs.pop("disabled", False) or self._being_submitted
            )
            if has_label:
                control = control_fn(*label, name=name, disabled=disabled, **kwargs)
            else:
                control = control_fn(name=name, disabled=disabled, **kwargs)

        if self._submit_clicked:
            fc.validate()

        return control

    def __exit__(self, *args, **kwargs):
        super().__exit__(*args, **kwargs)

        pending = False
        valid = True
        is_async = False

        for fc in self.form_controls:
            pending = pending or fc.is_pending()
            valid = valid and fc.is_valid()
            is_async = is_async or fc.is_async

        self.is_valid = valid

        if not pending:
            if self._being_submitted:
                if is_async:
                    self.trigger_event("_async_resubmitted", True)
                self._being_submitted = False

    def checkbox(self, *label, wrapper_style=None, **kwargs):
        """
        Adds a @component(checkbox) component to the form.

        The `wrapper_style` argument can be a @component(style)
        instance to control the style style of the internal container
        that wraps the form input + the validation error message.

        The `**kwargs` are passed on to the @component(checkbox)
        constructor.

        """
        return self._form_control(
            checkbox, *label, wrapper_style=wrapper_style, **kwargs
        )

    def color_picker(self, wrapper_style=None, **kwargs):
        """Adds a @component(color_picker) component to the form."""
        return self._form_control(
            color_picker, has_label=False, wrapper_style=wrapper_style, **kwargs
        )

    def text_input(self, *label, wrapper_style=None, **kwargs):
        """Adds a @component(text_input) component to the form."""
        return self._form_control(
            text_input, *label, wrapper_style=wrapper_style, **kwargs
        )

    def textarea(self, *label, wrapper_style=None, **kwargs):
        """Adds a @component(textarea) component to the form."""
        return self._form_control(
            textarea, *label, wrapper_style=wrapper_style, **kwargs
        )

    def radio_group(self, *label, wrapper_style=None, **kwargs):
        """Adds a @component(radio_group) component to the form."""
        return self._form_control(
            radio_group, *label, wrapper_style=wrapper_style, **kwargs
        )

    def slider(self, *label, wrapper_style=None, **kwargs):
        """Adds a @component(slider) component to the form."""
        return self._form_control(slider, *label, wrapper_style=wrapper_style, **kwargs)

    def select(self, *label, wrapper_style=None, **kwargs):
        """Adds a @component(select) component to the form."""
        return self._form_control(select, *label, wrapper_style=wrapper_style, **kwargs)

    def switch(self, *label, wrapper_style=None, **kwargs):
        """Adds a @component(switch) component to the form."""
        return self._form_control(switch, *label, wrapper_style=wrapper_style, **kwargs)

    def submit_button(self, *label, **kwargs):
        """
        Adds a @component(button) component to the form with
        `type="submit"`. When this button is clicked, the form is
        submitted for validation. If validation passes,
        `form.submitted` becomes `True`. Otherwise, validation
        messages are shown to the user on any field that failed
        validation.

        If the label is omitted it is automatically set to `"Submit"`.

        """
        if not label:
            label = ("Submit",)
        disabled = (
            self.disabled or kwargs.pop("disabled", False) or self._being_submitted
        )
        return button(*label, button_type="submit", disabled=disabled, **kwargs)

    def reset_button(self, *label, **kwargs):
        """
        Adds a @component(button) component to the form. When this button
        is clicked, all fields in the form are reset.

        If the label is omitted, it is automatically set to `"Reset"`.
        """
        if not label:
            label = ("Reset",)
        disabled = (
            self.disabled or kwargs.pop("disabled", False) or self._being_submitted
        )
        reset_button = button(*label, disabled=disabled, **kwargs)
        if reset_button.clicked:
            self.reset()

    def submit(self):
        """
        A way to programmatically submit the form.
        """
        if self._being_submitted:
            logger.warn("A submit request is already being processed.")
            return
        self.trigger_event("_submit_clicked", True)

    def reset(self):
        """
        A way to programmatically reset the form.
        """
        if self._being_submitted:
            logger.warn("Cannot reset a form while it is submitting.")
            return
        for fc in self.form_controls:
            fc.reset()
