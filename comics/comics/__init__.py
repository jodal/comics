import os


def get_comic_module_names():
    module_files = os.listdir(os.path.dirname(__file__))
    module_names = []
    for file in module_files:
        if file.endswith(".py") and not file.startswith("__init__"):
            module_names.append(file.replace(".py", ""))
    return sorted(module_names)


def get_comic_module(comic_slug):
    module_name = "%s.%s" % (__package__, comic_slug)
    return _import_by_name(module_name)


def _import_by_name(module_name):
    module = __import__(module_name)
    components = module_name.split(".")
    for component in components[1:]:
        module = getattr(module, component)
    return module
