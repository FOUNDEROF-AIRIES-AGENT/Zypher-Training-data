"""Coltex Plugin SDK — extend processors, connectors, curators, and more."""

from __future__ import annotations

from typing import Any, Callable

from runtime.plugins.manager import PluginManager

Handler = Callable[..., Any]

_registry: PluginManager | None = None


def init(manager: PluginManager) -> None:
    global _registry
    _registry = manager


def register_connector(plugin_id: str, handler: Handler) -> None:
    _require().register(f"connector:{plugin_id}", handler)


def register_processor(plugin_id: str, handler: Handler) -> None:
    _require().register(f"processor:{plugin_id}", handler)


def register_curator(plugin_id: str, handler: Handler) -> None:
    _require().register(f"curator:{plugin_id}", handler)


def register_embedding_model(plugin_id: str, handler: Handler) -> None:
    _require().register(f"embedding:{plugin_id}", handler)


def register_search_algorithm(plugin_id: str, handler: Handler) -> None:
    _require().register(f"search:{plugin_id}", handler)


def subscribe_event(event_id: str, handler: Handler) -> None:
    _require().register(f"event:{event_id}", handler)


def _require() -> PluginManager:
    if _registry is None:
        raise RuntimeError("Plugin SDK not initialized — call init() from ColtexRuntime first")
    return _registry
