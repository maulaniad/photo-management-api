from django.urls import path, include


urlpatterns = [
    path("authentication/", include("api.authentication.urls", namespace="authentication")),
    path("profile/", include("api.profile.urls", namespace="profile")),
    path("session/", include("api.session.urls", namespace="session")),
    path("user/", include("api.user.urls", namespace="user")),
]
