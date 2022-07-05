"""This module implements a handler for the Python language."""

from __future__ import annotations

from typing import Any

from markdown import Markdown
from markupsafe import Markup
from mkdocs.exceptions import PluginError
from mkdocstrings.handlers.base import BaseHandler, CollectionError, CollectorItem
from mkdocstrings.loggers import get_logger


logger = get_logger(__name__)


class TypescriptHandler(BaseHandler):
    """The Typescript handler class.

    Attributes:
        domain: The cross-documentation domain/language for this handler.
        enable_inventory: Whether this handler is interested in enabling the creation
            of the `objects.inv` Sphinx inventory file.
        fallback_theme: The theme to fallback to.
        fallback_config: The configuration used to collect item during autorefs fallback.
        default_config: The default configuration option,
            see [`default_config`][mkdocstrings_handlers.typescript.handler.TypescriptHandler.default_config].
    """

    domain: str = "typescript"  # to match Sphinx's default domain
    enable_inventory: bool = False
    fallback_theme = "material"
    fallback_config: dict = {"fallback": True}
    default_config: dict = {
        "show_root_heading": False,
        "show_root_toc_entry": True,
        "heading_level": 2,
    }
    """The default configuration options.

    Option | Type | Description | Default
    ------ | ---- | ----------- | -------
    **`show_root_heading`** | `bool` | Show the heading of the object at the root of the documentation tree. | `False`
    **`show_root_toc_entry`** | `bool` | If the root heading is not shown, at least add a ToC entry for it. | `True`
    **`show_source`** | `bool` | Show the source code of this object. | `True`
    **`heading_level`** | `int` | The initial heading level to use. | `2`
    """  # noqa: E501

    def collect(self, identifier: str, config: dict) -> CollectorItem:  # noqa: D102
        pass

    def render(self, data: CollectorItem, config: dict) -> str:  # noqa: D102
        pass

    def update_env(self, md: Markdown, config: dict) -> None:  # noqa: D102 (ignore missing docstring)
        super().update_env(md, config)
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False
        self.env.filters["crossref"] = self.do_crossref

    def do_crossref(self, path: str, brief: bool = True) -> Markup:
        """Filter to create cross-references.

        Parameters:
            path: The path to link to.
            brief: Show only the last part of the path, add full path as hover.

        Returns:
            Markup text.
        """
        full_path = path
        if brief:
            path = full_path.split(".")[-1]
        return Markup("<span data-autorefs-optional-hover={full_path}>{path}</span>").format(
            full_path=full_path, path=path
        )


def get_handler(
    theme: str,  # noqa: W0613 (unused argument config)
    custom_templates: str | None = None,
    config_file_path: str | None = None,
    **config: Any,
) -> TypescriptHandler:
    """Simply return an instance of `TypescriptHandler`.

    Arguments:
        theme: The theme to use when rendering contents.
        custom_templates: Directory containing custom templates.
        config_file_path: The MkDocs configuration file path.
        **config: Configuration passed to the handler.

    Returns:
        An instance of the handler.
    """
    return TypescriptHandler(
        handler="typescript",
        theme=theme,
        custom_templates=custom_templates,
        config_file_path=config_file_path,
    )
