import os
from types import ModuleType
from typing import List


def get_comic_module_names() -> List[str]:
    module_files = os.listdir(os.path.dirname(__file__))
    module_names = []
    for file in module_files:
        if file.endswith(".py") and not file.startswith("__init__"):
            module_names.append(file.replace(".py", ""))
    return sorted(module_names)


def get_comic_module(comic_slug: str) -> ModuleType:
    module_name = f"{__package__}.{comic_slug}"
    return _import_by_name(module_name)


def _import_by_name(module_name: str) -> ModuleType:
    module = __import__(module_name)
    components = module_name.split(".")
    for component in components[1:]:
        module = getattr(module, component)
    assert isinstance(module, ModuleType)
    return module
