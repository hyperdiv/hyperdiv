from .component_base import BaseState

global_key_id = 0


def global_state(klass):
    """
    `global_state` is a decorator that can be be used to define a
    state component class such that all instances of that class share
    the same underlying state.

    This can be handy when a state component is used by many
    functions, and you want to avoid explicitly passing the state
    component into all those functions.

    This decorator can be used on subclasses of @component(BaseState) and
    @component(task).

    ```py-nodemo
    @hd.global_state
    class MyState(hd.BaseState):
        count = hd.Prop(hd.Int, 0)

    def increment():
        state = MyState()
        if hd.button("Increment").clicked:
            state.count += 1

    def display():
        state = MyState()
        hd.text(state.count)

    def main():
        increment()
        display()
    ```

    In this example, both `MyState()` instances share the same
    state. So when the increment button in the `increment` component
    is clicked, the count label displayed by the `display` component
    is updated.

    ## Use with `task`

    The `global_state` decorator can also be used on a subclass of
    @component(task) to make a task global.

    ```py-nodemo
    @hd.global_state
    class UsersTask(hd.task):
        def run(self):
            super().run(sql, "select * from Users")

    def users_list():
        task = UsersTask()
        task.run()
        if task.result:
            for u in task.result:
                with hd.scope(u.user_id):
                    hd.text(u.name)

    def reload_button():
        task = UsersTask()
        if hd.button("Reload").clicked:
            task.clear()

    def main():
        users_list()
        reload_button()
    ```

    In this example, both instances of `UsersTask()` share the same task
    state. When the `Reload` button in `reload_button` is clicked, the
    task re-runs and the users list in `users_list` is re-rendered.

    """
    global global_key_id
    if not issubclass(klass, BaseState):
        raise ValueError("You cannot use `@global_component` with this class.")
    klass._key = f"global-state-{global_key_id}"
    global_key_id += 1
    return klass
