from __future__ import annotations

import importlib
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import ModuleType


def get_comic_module_names() -> list[str]:
    module_names = [
        file.stem
        for file in Path(__file__).parent.glob("*.py")
        if not file.name.startswith("__init__")
    ]
    return sorted(module_names)


def get_comic_module(comic_slug: str) -> ModuleType:
    module_name = f"{__package__}.{comic_slug}"
    return importlib.import_module(module_name)
