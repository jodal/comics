from django.conf import settings

def get_comic_module(comic_slug):
    module_name = '%s.%s' % (settings.COMICS_CRAWLER_PACKAGE, comic_slug)
    return _import_by_name(module_name)

def _import_by_name(module_name):
    module = __import__(module_name)
    components = module_name.split('.')
    for component in components[1:]:
        module = getattr(module, component)
    return module
