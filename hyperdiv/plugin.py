import glob
from urllib.parse import urlparse
import os
from .component_base import Component
from .component_mixins.styled import Styled

PLUGINS_PREFIX = "/hyperdiv-plugins"


def is_url(s):
    try:
        result = urlparse(s)
        # Ensure the URL has at least a scheme (e.g., "http") and a netloc (e.g., "www.google.com")
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_path(s):
    return urlparse(s).path


def is_pure_path(s):
    result = urlparse(s)
    return result.path and not (
        result.scheme
        or result.netloc
        or result.params
        or result.query
        or result.fragment
    )


class PluginAssetsCollector(type):
    plugin_assets: dict = dict()

    def __new__(cls, clsname, bases, attrs):
        klass = super().__new__(cls, clsname, bases, attrs)

        if clsname != "Plugin":
            plugin_name = getattr(klass, "_name", None) or klass.__name__

            assets_root = getattr(klass, "_assets_root", None)
            asset_descriptions = getattr(klass, "_assets", None)

            def check_assets_root():
                if not assets_root:
                    raise Exception(
                        f"Plugin {plugin_name} does not specify an `_assets_root`"
                    )

                if not os.path.exists(assets_root):
                    raise Exception(
                        f"Plugin {plugin_name} `_assets_root` {assets_root} does not exist."
                    )

                if not os.path.isabs(assets_root):
                    raise Exception(
                        f"Plugin {plugin_name} `_assets_root` {assets_root} is not an absolute path."
                    )

            def infer_asset_from_extension(asset):
                asset_path = get_path(asset)
                if asset_path.lower().endswith(".css"):
                    return ("css-link", asset)
                elif asset_path.lower().endswith(".js"):
                    return ("js-link", asset)
                else:
                    raise Exception(f"Asset with unknown extension: {asset}")

            if not asset_descriptions:
                raise Exception(f"Plugin {plugin_name} does not specify any `_assets`.")

            if assets_root:
                check_assets_root()

            assets_config = dict(
                assets_root=assets_root,
                assets=[],
            )

            for asset_description in asset_descriptions:
                if isinstance(asset_description, tuple):
                    if len(asset_description) != 2:
                        raise Exception(f"Invalid asset: {asset_description}")
                    typ, asset = asset_description
                    if typ in ("js", "css"):
                        assets_config["assets"].append(asset_description)
                        continue
                    if typ not in ("css-link", "js-link"):
                        raise Exception(f"Invalid asset type: {typ}")
                    if not is_url(asset):
                        check_assets_root()
                        asset_path = get_path(asset)
                        if not os.path.exists(os.path.join(assets_root, asset_path)):
                            raise Exception(
                                f"Plugin asset path {asset_path} does not exist."
                            )
                    assets_config["assets"].append(asset_description)
                elif is_url(asset_description):
                    assets_config["assets"].append(
                        infer_asset_from_extension(asset_description)
                    )
                elif not is_pure_path(asset_description):
                    check_assets_root()
                    asset_path = get_path(asset_description)
                    if not os.path.exists(os.path.join(assets_root, asset_path)):
                        raise Exception(
                            f"Plugin asset path {asset_path} does not exist."
                        )
                    print(
                        asset_description,
                        asset_path,
                        infer_asset_from_extension(asset_description),
                    )
                    assets_config["assets"].append(
                        infer_asset_from_extension(asset_description)
                    )
                else:
                    check_assets_root()
                    paths = glob.glob(
                        asset_description, root_dir=assets_root, recursive=True
                    )
                    if not paths:
                        raise Exception(
                            f"Asset description {asset_description} did not match any files."
                        )
                    for path in paths:
                        assets_config["assets"].append(infer_asset_from_extension(path))

            PluginAssetsCollector.plugin_assets[plugin_name] = assets_config

        return klass


class Plugin(Component, Styled, metaclass=PluginAssetsCollector):
    """
    This class can be subclassed to define custom Hyperdiv components,
    with custom Javascript, CSS, and other assets, such as images.

    See [here](/extending-hyperdiv/plugins) for a detailed dive into how
    plugins work.
    """

    _tag = "hyperdiv-plugin"
    _camlcase_props = False

    @staticmethod
    def js(asset):
        """Helper to define an inline Javascript asset."""
        return ("js", asset)

    @staticmethod
    def css(asset):
        """Helper to define an inline CSS asset."""
        return ("css", asset)

    @staticmethod
    def js_link(asset):
        """Helper to define a Javascript link asset."""
        return ("js-link", asset)

    @staticmethod
    def css_link(asset):
        """Helper to define a CSS link asset."""
        return ("css-link", asset)

    def render(self):
        """
        The JSON-rendered form of the plugin that is sent to the browser.
        """
        klass = type(self)
        plugin_name = getattr(klass, "_name", None) or klass.__name__

        plugin_config = PluginAssetsCollector.plugin_assets.get(plugin_name, {})

        assets_root = plugin_config.get("assets_root")
        assets_paths = plugin_config.get("assets", [])

        output = super().render()

        if assets_root:
            output["assetsRoot"] = f"{PLUGINS_PREFIX}/{plugin_name}"

        output["assets"] = []

        for asset_type, asset_path in assets_paths:
            if asset_type in ("css", "js") or is_url(asset_path):
                output["assets"].append((asset_type, asset_path))
            else:
                output["assets"].append(
                    (asset_type, f"{PLUGINS_PREFIX}/{plugin_name}/{asset_path}")
                )

        return output
