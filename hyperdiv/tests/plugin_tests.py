import pytest
import tempfile
import os
from ..test_utils import mock_frame
from ..plugin import Plugin, PluginAssetsCollector, PLUGINS_PREFIX


def test_plugin_incomplete_spec():
    # No assets specified
    with pytest.raises(Exception):

        class BadPlugin1(Plugin):
            pass

    # Specifying local assets with _asset_root
    with pytest.raises(Exception):

        class BadPlugin2(Plugin):
            _assets = ["foo.js"]

    # Nonexisting asset root
    with pytest.raises(Exception):

        class BadPlugin3(Plugin):
            _assets_root = "foo"
            _assets = ["foo.js"]

    # Nonexisting asset root
    with pytest.raises(Exception):

        class BadPlugin4(Plugin):
            _assets_root = "foo"
            _assets = ["foo.js"]

    # Unknown extension
    with pytest.raises(Exception):

        class BadPlugin5(Plugin):
            _assets = ["https://foo.com/foo.bar"]

    # Bad asset type
    with pytest.raises(Exception):

        class BadPlugin6(Plugin):
            _assets = [("bad-type", "https://foo.com/foo.js")]

    # Too many description components
    with pytest.raises(Exception):

        class BadPlugin7(Plugin):
            _assets = [("js-link", "https://foo.com/foo.js", "bar")]


@mock_frame
def test_plugin_nonexisting_local_asset():
    with tempfile.TemporaryDirectory() as plugin_dir:

        with pytest.raises(Exception):

            class BadPlugin8(Plugin):
                _assets_root = plugin_dir
                _assets = ["plugin.js"]

        with pytest.raises(Exception):

            class BadPlugin9(Plugin):
                _assets_root = plugin_dir
                _assets = [Plugin.js_link("plugin.js")]


@mock_frame
def test_plugin_remote_assets():
    # Remote assets without _assert_root is OK
    class Plugin3(Plugin):
        _assets = ["https://foo.com/foo.js", "https://foo.com/foo.css"]

    assert "Plugin3" in PluginAssetsCollector.plugin_assets
    assert set(PluginAssetsCollector.plugin_assets["Plugin3"]["assets"]) == set(
        [
            Plugin.js_link("https://foo.com/foo.js"),
            Plugin.css_link("https://foo.com/foo.css"),
        ]
    )

    p = Plugin3()
    rendered = p.render()
    assert set(rendered["assets"]) == set(
        [
            Plugin.js_link("https://foo.com/foo.js"),
            Plugin.css_link("https://foo.com/foo.css"),
        ]
    )


@mock_frame
def test_plugin_local_assets():
    with tempfile.TemporaryDirectory() as plugin_dir:
        with open(os.path.join(plugin_dir, "plugin.js"), "w") as f:
            f.write('console.log("Hello");')
        with open(os.path.join(plugin_dir, "plugin.css"), "w") as f:
            f.write(".foo { margin: 0 }")

        class Plugin4(Plugin):
            _assets_root = plugin_dir
            _assets = [Plugin.js_link("plugin.js"), Plugin.css_link("plugin.css")]

        assert "Plugin4" in PluginAssetsCollector.plugin_assets
        assert (
            PluginAssetsCollector.plugin_assets["Plugin4"]["assets_root"] == plugin_dir
        )
        assert set(PluginAssetsCollector.plugin_assets["Plugin4"]["assets"]) == set(
            [Plugin.js_link("plugin.js"), Plugin.css_link("plugin.css")]
        )

        p = Plugin4()
        rendered = p.render()
        assert set(rendered["assets"]) == set(
            [
                Plugin.js_link(f"{PLUGINS_PREFIX}/Plugin4/plugin.js"),
                Plugin.css_link(f"{PLUGINS_PREFIX}/Plugin4/plugin.css"),
            ]
        )


@mock_frame
def test_plugin_assets_glob():
    with tempfile.TemporaryDirectory() as plugin_dir:
        os.makedirs(os.path.join(plugin_dir, "a", "b", "c"))
        os.makedirs(os.path.join(plugin_dir, "x", "y"))

        with open(os.path.join(plugin_dir, "a", "b", "c", "js1.js"), "w") as f:
            f.write('console.log("Hello 1");')
        with open(os.path.join(plugin_dir, "a", "b", "js2.js"), "w") as f:
            f.write('console.log("Hello 2");')
        with open(os.path.join(plugin_dir, "x", "y", "style.css"), "w") as f:
            f.write(".foo { margin: 0 }")

        class Plugin4(Plugin):
            _assets_root = plugin_dir
            _assets = ["**/*.js", "**/*.css"]

        assert "Plugin4" in PluginAssetsCollector.plugin_assets
        assert (
            PluginAssetsCollector.plugin_assets["Plugin4"]["assets_root"] == plugin_dir
        )
        assert set(PluginAssetsCollector.plugin_assets["Plugin4"]["assets"]) == set(
            [
                Plugin.js_link("a/b/c/js1.js"),
                Plugin.js_link("a/b/js2.js"),
                Plugin.css_link("x/y/style.css"),
            ]
        )

        p = Plugin4()
        rendered = p.render()

        assert set(rendered["assets"]) == set(
            [
                Plugin.js_link(f"{PLUGINS_PREFIX}/Plugin4/a/b/c/js1.js"),
                Plugin.js_link(f"{PLUGINS_PREFIX}/Plugin4/a/b/js2.js"),
                Plugin.css_link(f"{PLUGINS_PREFIX}/Plugin4/x/y/style.css"),
            ]
        )


@mock_frame
def test_plugin_inline_assets():
    inline_js = "console.log('Hello World');"
    inline_css = ".foo { margin: 0}"

    class Plugin5(Plugin):
        _assets = [Plugin.js(inline_js), Plugin.css(inline_css)]

    assert "Plugin5" in PluginAssetsCollector.plugin_assets
    assert set(PluginAssetsCollector.plugin_assets["Plugin5"]["assets"]) == set(
        [Plugin.js(inline_js), Plugin.css(inline_css)]
    )

    p = Plugin5()
    rendered = p.render()
    assert set(rendered["assets"]) == set(
        [Plugin.js(inline_js), Plugin.css(inline_css)]
    )


@mock_frame
def test_mixed_assets():
    inline_js = "console.log('Hello World');"
    inline_css = ".foo { margin: 0}"

    with tempfile.TemporaryDirectory() as plugin_dir:
        os.makedirs(os.path.join(plugin_dir, "a", "b", "c"))

        with open(os.path.join(plugin_dir, "a", "b", "c", "plugin.js"), "w") as f:
            f.write("console.log('Hello World');")
        with open(os.path.join(plugin_dir, "style.css"), "w") as f:
            f.write(".foo { margin: 0 }")

        class Plugin6(Plugin):
            _assets_root = plugin_dir
            _assets = [
                "**/*.js",
                "style.css?x=1",
                Plugin.js(inline_js),
                Plugin.css(inline_css),
                "https://foo.com/script.js?x=1#foo",
                "https://foo.com/style.css",
            ]

        assert "Plugin6" in PluginAssetsCollector.plugin_assets
        assert (
            PluginAssetsCollector.plugin_assets["Plugin6"]["assets_root"] == plugin_dir
        )
        assert set(PluginAssetsCollector.plugin_assets["Plugin6"]["assets"]) == set(
            [
                Plugin.js(inline_js),
                Plugin.css(inline_css),
                Plugin.js_link("a/b/c/plugin.js"),
                Plugin.css_link("style.css?x=1"),
                Plugin.js_link("https://foo.com/script.js?x=1#foo"),
                Plugin.css_link("https://foo.com/style.css"),
            ]
        )

        p = Plugin6()
        rendered = p.render()
        assert set(rendered["assets"]) == set(
            [
                Plugin.js(inline_js),
                Plugin.css(inline_css),
                Plugin.js_link(f"{PLUGINS_PREFIX}/Plugin6/a/b/c/plugin.js"),
                Plugin.css_link(f"{PLUGINS_PREFIX}/Plugin6/style.css?x=1"),
                Plugin.js_link("https://foo.com/script.js?x=1#foo"),
                Plugin.css_link("https://foo.com/style.css"),
            ]
        )


@mock_frame
def test_assets_root():
    with tempfile.TemporaryDirectory() as plugin_dir:

        class Plugin7(Plugin):
            _assets_root = plugin_dir
            _assets = ["https://foo.com/foo.js"]

        assert (
            PluginAssetsCollector.plugin_assets["Plugin7"]["assets_root"] == plugin_dir
        )

        p = Plugin7()
        rendered = p.render()

        assert rendered["assetsRoot"] == f"{PLUGINS_PREFIX}/Plugin7"

    class Plugin8(Plugin):
        _assets = ["https://foo.com/foo.js"]

    assert PluginAssetsCollector.plugin_assets["Plugin8"]["assets_root"] is None

    p = Plugin8()
    rendered = p.render()

    assert "assetsRoot" not in rendered
