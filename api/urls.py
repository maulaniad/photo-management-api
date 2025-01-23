from django.urls import path, include


urlpatterns = [
    path("auth/", include("api.authentication.urls", namespace="authentication")),
    path("user/", include("api.user.urls", namespace="user")),
    path("profile/", include("api.profile.urls", namespace="profile")),
]
