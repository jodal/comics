from django.urls import path


def fail(request):
    # Useful for e.g. testing Sentry integration
    1 / 0


urlpatterns = [
    path("fail/", fail),
]
