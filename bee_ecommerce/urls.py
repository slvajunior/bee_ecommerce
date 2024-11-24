from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Importando o redirecionamento


urlpatterns = [
    path("admin/", admin.site.urls),
    path("store/", include("store.urls")),  # Incluir as URLs do app store
    path(
        "", RedirectView.as_view(url="/store/", permanent=True)
    ),  # Redireciona a raiz para /store/
]
