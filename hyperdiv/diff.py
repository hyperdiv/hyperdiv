from .frame import RenderFrame


class Diff:
    def __init__(self):
        self._diff = []

    def add_component_diff(self, component_diff):
        self._diff.append(component_diff)

    def render(self):
        output = dict()
        for component_diff in self._diff:
            output[component_diff.key] = component_diff.render()
        return output

    def is_empty(self):
        return len(self._diff) == 0


class ComponentDiff:
    def __init__(self, key, props):
        self.key = key
        self.props = props
        self.children = []

    def add_command(self, command):
        self.children.append(command)

    def is_empty(self):
        return len(self.props) == 0 and len(self.children) == 0

    def render(self):
        from .renderer import render_props

        output = dict()
        if len(self.props) > 0:
            output |= render_props(self.key, self.props)
        if len(self.children) > 0:
            output["children"] = [command.render() for command in self.children]
        return output


class Insert:
    def __init__(self, start_idx, components):
        self.start_idx = start_idx
        self.components = components

    def render(self):
        return (
            "insert",
            self.start_idx,
            tuple(component.render() for component in self.components),
        )


class Delete:
    def __init__(self, start_idx, num_items):
        self.start_idx = start_idx
        self.num_items = num_items

    def render(self):
        return ("delete", self.start_idx, self.num_items)


class Differ:
    def __init__(self):
        self.frame = RenderFrame.current()
        self.diff = Diff()

    def diff_component(self, src_component, dest_component):
        if src_component == dest_component:
            # This means the component was cached. The source and
            # destination are identical, so there's nothing to diff.
            return

        key = dest_component._key

        props = self.frame.get_props(key).values()

        # TODO: We currently don't properly diff CSS. If any CSS prop
        # changed, we re-render all CSS props.
        css_was_updated = False
        for prop in props:
            if self.frame.prop_changed(prop) and prop.is_css_prop:
                css_was_updated = True
                break

        changed_props = [
            prop
            for prop in props
            if not prop.internal
            and self.frame.prop_changed(prop)
            or (prop.is_css_prop and css_was_updated)
        ]

        diff = ComponentDiff(key, changed_props)

        if src_component._has_children:
            self.diff_children(diff, src_component._children, dest_component._children)

        if not diff.is_empty():
            self.diff.add_component_diff(diff)

    def diff_children(self, diff, src, dest):
        src_idx = 0
        dest_idx = 0

        def emit_insert(start_idx, component_list):
            diff.add_command(Insert(start_idx, component_list))

        def emit_delete(start_idx, num_items):
            diff.add_command(Delete(start_idx, num_items))

        while True:
            try:
                src_elem = src[src_idx]
            except IndexError:
                if dest_idx < len(dest):
                    emit_insert(dest_idx, dest[dest_idx:])
                break

            try:
                dest_elem = dest[dest_idx]
            except IndexError:
                emit_delete(dest_idx, len(src) - src_idx)
                break

            if src_elem._key == dest_elem._key:
                self.diff_component(src_elem, dest_elem)
                src_idx += 1
                dest_idx += 1
            else:
                si = src_idx
                di = dest_idx

                # maps key to index in the array
                seen_in_source = dict()
                seen_in_dest = dict()

                found = False

                while di < len(dest) or si < len(src):
                    if si < len(src):
                        if src[si]._key in seen_in_dest:
                            di = seen_in_dest[src[si]._key]
                            found = True
                            break
                        else:
                            seen_in_source[src[si]._key] = si
                            si += 1

                    if di < len(dest):
                        if dest[di]._key in seen_in_source:
                            si = seen_in_source[dest[di]._key]
                            found = True
                            break
                        else:
                            seen_in_dest[dest[di]._key] = di
                            di += 1

                if found:
                    if si - src_idx > 0:
                        emit_delete(dest_idx, si - src_idx)

                    to_insert = dest[dest_idx:di]
                    if len(to_insert) > 0:
                        emit_insert(dest_idx, to_insert)

                    src_idx = si
                    dest_idx = di

                    continue

                emit_delete(dest_idx, len(src) - src_idx)
                emit_insert(dest_idx, dest[dest_idx:])
                break

    def diff_mutations(self, mutations):
        for key, prop_name in mutations:
            props = self.frame.get_props(key)

            prop = props[prop_name]

            if prop.internal:
                continue

            if self.frame.prop_changed(prop):
                changed_props = [prop]
                if prop.is_css_prop:
                    for prop in props:
                        if prop.is_css_prop:
                            changed_props.append(prop)
                self.diff.add_component_diff(ComponentDiff(key, changed_props))


def diff_mutations(mutations):
    d = Differ()
    d.diff_mutations(mutations)
    if not d.diff.is_empty():
        return d.diff


def diff(previous_component, component):
    d = Differ()
    d.diff_component(previous_component, component)
    if not d.diff.is_empty():
        return d.diff
