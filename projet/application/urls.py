from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from aliment.views import v_accueil

urlpatterns = [
    path("", v_accueil.index, name="index"),
    path("aliment/", include("aliment.urls")),
    path("espace_admin/", include("espace_admin.urls")),
    path("user/", include("utilisateur.urls")),
    # path('api/', include('api.urls')),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
