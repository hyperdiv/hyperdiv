from urllib.parse import urlparse
import os
from .component_base import Component

PLUGINS_PREFIX = "/hyperdiv-plugins"


def is_url(s):
    try:
        result = urlparse(s)
        # Ensure the URL has at least a scheme (e.g., "http") and a netloc (e.g., "www.google.com")
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class PluginAssetsCollector(type):
    plugin_assets: dict = dict()

    def __new__(cls, clsname, bases, attrs):
        klass = super().__new__(cls, clsname, bases, attrs)

        if clsname != "Plugin":
            plugin_name = getattr(klass, "_name", None) or klass.__name__

            assets_root = getattr(klass, "assets_root", None)
            assets = getattr(klass, "assets", None)

            if not assets:
                raise Exception(f"Plugin {plugin_name} does not specify any `assets`.")

            local_assets = []
            for typ, asset in klass.assets:
                if typ in ("css-link", "js-link"):
                    if not is_url(asset):
                        local_assets.append((typ, asset))

            if not local_assets:
                return

            if not assets_root:
                raise Exception(
                    f"Plugin {plugin_name} does not specify an `assets_root`"
                )

            if not os.path.exists(assets_root):
                raise Exception(
                    f"Plugin {plugin_name} `assets_root` {assets_root} does not exist."
                )

            if not os.path.isabs(assets_root):
                raise Exception(
                    f"Plugin {plugin_name} `assets_root` {assets_root} is not an absolute path."
                )

            assets_config = dict(
                assets_root=assets_root,
                assets=[],
            )

            PluginAssetsCollector.plugin_assets[plugin_name] = assets_config

            for typ, asset_path in local_assets:
                if typ in ("css-link", "js-link"):
                    path = os.path.join(assets_root, asset_path)
                    if not os.path.exists(path):
                        raise Exception(
                            f"Asset path {asset_path} specified by plugin {plugin_name} does not exist."
                        )

                    assets_config["assets"].append(asset_path)

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
        klass = type(self)
        plugin_name = getattr(klass, "_name", None) or klass.__name__

        asset_paths = PluginAssetsCollector.plugin_assets.get(plugin_name, {}).get(
            "assets", []
        )

        output = super().render()
        output["assets"] = []

        for asset_type, asset in type(self).assets:
            if asset in asset_paths:
                output["assets"].append(
                    (asset_type, f"{PLUGINS_PREFIX}/{plugin_name}/{asset}")
                )
            else:
                output["assets"].append((asset_type, asset))

        return output
