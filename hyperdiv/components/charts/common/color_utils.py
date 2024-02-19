from ....prop_types import Color

auto_colors = [
    "blue",
    "orange",
    "green",
    "red",
    "yellow",
    "purple",
    "neutral",
    "amber",
    "fuchsia",
    "violet",
    "lime",
    "pink",
    "teal",
]


def auto_color_generator():
    i = 0
    while True:
        if i >= len(auto_colors):
            i = 0
        yield auto_colors[i]
        i += 1


def get_auto_colors(num_colors):
    gen = auto_color_generator()
    return [next(gen) for _ in range(num_colors)]


def pad_colors(colors, maxlen):
    auto_cols = get_auto_colors(maxlen)

    out_colors = []

    for i in range(maxlen):
        out_colors.append(colors[i] if colors and i < len(colors) else auto_cols[i])

    return [Color.render(Color.parse(c)) for c in out_colors]
