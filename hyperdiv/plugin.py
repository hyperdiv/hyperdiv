from urllib.parse import urlparse
import os
from .component_base import Component


def is_url(s):
    try:
        result = urlparse(s)
        # Ensure the URL has at least a scheme (e.g., "http") and a netloc (e.g., "www.google.com")
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class PluginAssetsCollector(type):
    plugin_assets: dict[str, str] = dict()

    def __new__(cls, clsname, bases, attrs):
        klass = super().__new__(cls, clsname, bases, attrs)

        if clsname != "Plugin":
            plugin_name = getattr(klass, "_name", None) or klass.__name__

            for typ, asset in klass._assets:
                if typ in ("css-link", "js-link"):
                    if is_url(asset):
                        continue
                    if not os.path.exists(asset):
                        raise Exception(
                            f'Asset "{asset}" is neither a URL nor a local file.'
                        )
                    file_name = os.path.split(asset)[1]
                    PluginAssetsCollector.plugin_assets[
                        f"{plugin_name}/{file_name}"
                    ] = asset

        return klass


class Plugin(Component, metaclass=PluginAssetsCollector):
    _tag = "hyperdiv-plugin"

    @staticmethod
    def js(asset):
        return ("js", asset)

    @staticmethod
    def css(asset):
        return ("css", asset)

    @staticmethod
    def js_link(asset):
        return ("js-link", asset)

    @staticmethod
    def css_link(asset):
        return ("css-link", asset)

    def render(self):
        reverse_map = {
            value: key for key, value in PluginAssetsCollector.plugin_assets.items()
        }

        output = super().render()
        assets = type(self)._assets
        output["assets"] = [
            (
                asset_type,
                f"/plugins/{reverse_map[asset]}" if asset in reverse_map else asset,
            )
            for (asset_type, asset) in assets
        ]
        return output
