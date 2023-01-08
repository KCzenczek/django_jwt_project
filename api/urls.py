from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views import UserList


urlpatterns = [
    path("v0/user-list", UserList.as_view(), name="user-list"),
    path("v0/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger_ui"),
    path("v0/schema/", SpectacularAPIView.as_view(), name="schema"),
]