import os
import inspect
import xxhash
from .frame import AppRunnerFrame

runtime_py_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "app_runner.py"
)


def validate_component_key(key):
    key = str(key)
    if len(key) == 0 or not key[0].isalpha():
        return False
    for char in key:
        if not char.isalnum() and char not in ("-", "_"):
            return False
    return True


def register_component_key(key):
    hyperdiv_frame = AppRunnerFrame.current()
    if key in hyperdiv_frame.keys:
        raise Exception("Duplicate key, perhaps missing scope()")
    hyperdiv_frame.keys.add(key)


def get_component_key(key=None):
    """Generate a unique component key from the filenames and line numbers
    of the pertinent functions currently on the stack. It tries to
    limit the search to user-defined code and avoid traversing the
    whole stack.
    """

    # Assumes `get_component_key` is called from a hyperdiv component
    # definition. `f_back.f_back` then skips (a) the call to this
    # function and (b) the call to the hyperdiv component, starting
    # the search at the point the user code called the hyperdiv
    # component.
    hyperdiv_frame = AppRunnerFrame.current()

    if not key:
        stack_frame = inspect.currentframe().f_back.f_back
        key = ""
        while stack_frame:
            filename = stack_frame.f_code.co_filename
            lineno = stack_frame.f_lineno
            funcname = stack_frame.f_code.co_name
            # It stops when it encounters `run_loop`, which the function
            # from which the user's app function is called.
            if filename == runtime_py_path and funcname == "run_user_app":
                break
            key += f"::{filename}:{lineno}:{funcname}"
            stack_frame = stack_frame.f_back

        key = str(hyperdiv_frame.scope_stack) + key
        # Prepend `a` because these keys are used as DOM IDs and a DOM ID
        # with a leading number is not valid.
        key = "a" + xxhash.xxh32(key).hexdigest()

    return key
