class Slot:
    def __init__(self, ui_name=None):
        self.name = None
        self.ui_name = ui_name.replace("_", "-") if ui_name else ui_name

    def __set_name__(self, klass, name):
        self.name = name
        if not self.ui_name:
            self.ui_name = self.name.replace("_", "-")

    def __get__(self, component, objtype):
        return self

    def __set__(self, component, value):
        raise Exception("Slots are read-only.")

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"<Slot {self.name}>"

    def __eq__(self, other):
        return (
            isinstance(other, Slot)
            and self.name == other.name
            and self.ui_name == other.ui_name
        )

    def __neq__(self, other):
        return (
            not isinstance(other, Slot)
            or self.name != other.name
            or self.ui_name != other.ui_name
        )
