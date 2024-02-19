from contextlib import contextmanager
from ..frame import AppRunnerFrame


def scope(scope_id):
    """
    When creating components in loops, you will encounter this error:

    ```py
    for i in range(3):
        hd.button("Button", i)
    ```

    To fix it, you wrap the loop body in `hd.scope(i)`, where `i`
    uniquely identifies each iteration:

    ```py
    for i in range(3):
        with hd.scope(i):
            hd.button("Button", i)
    ```

    The reason behind having to use `scope` is that Hyperdiv
    identifies each component uniquely based on the line number on
    which it is constructed, in the code. In the first example, all
    the buttons are constructed on the same line of code, so their
    identifiers clash and Hyperdiv raises an error.

    `hd.scope(i)` gives Hyperdiv extra "uniqueness" information to
    include in the identifier. In this case, `i` is unique for each
    loop iteration, allowing Hyperdiv to create unique identifiers for
    the three buttons.

    ## Choosing Good Scope IDs

    Using the loop iteration index, like in the example above, is fine
    for data that does not change. For data that can be sorted,
    edited, or deleted, we need to use an identifier that is unique to
    each data item.

    ```py
    state = hd.state(users=(
        ("Mary", False),
        ("Joe", False),
        ("Amy", False)
    ))

    for i, (name, selected) in enumerate(state.users):
        with hd.scope(i):
            with hd.hbox():
                hd.text(name, width=10)
                hd.checkbox(checked=selected)

    with hd.hbox(gap=1):
        if hd.button("Reverse").clicked:
            state.users = tuple(reversed(state.users))
    ```

    In the example above, we render a list of users along with
    "selected" checkboxes associated with each user, in a loop wrapped
    in `scope(i)`, which is the iteration index.

    If you check the checkbox next to `Mary`, and then click `Reverse`,
    the list will be reversed but `Amy` will now be wrongly
    selected. This is because the checkbox identifier is derived from
    `hd.scope(i)`, and `i` remains the same regardless of how the list
    is sorted.

    To fix this, we associate a unique user ID with each user record,
    and use this ID as the scope ID:

    ```py
    state = hd.state(users=(
        (123, "Mary", False),
        (456, "Joe", False),
        (789, "Amy", False)
    ))

    for user_id, name, selected in state.users:
        with hd.scope(user_id):
            with hd.hbox():
                hd.text(name, width=10)
                hd.checkbox(checked=selected)

    with hd.hbox(gap=1):
        if hd.button("Reverse").clicked:
            state.users = tuple(reversed(state.users))
    ```

    When working with databases, this is an easy guideline to
    follow. When rendering a list of database records, wrap the loop
    body in a scope identified by each record's primary key:

    ```py-nodemo
    users = database.get_users()
    for user in users:
       with hd.scope(user.user_id):
         render_user(user)
    ```

    """

    @contextmanager
    def scope_generator():
        frame = AppRunnerFrame.current()
        frame.push_scope(scope_id)
        try:
            yield
        finally:
            frame.pop_scope()

    return scope_generator()
