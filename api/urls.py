from django.urls import path, include


urlpatterns = [
    path("auth/", include("api.authentication.urls", namespace="authentication")),
    path("profile/", include("api.profile.urls", namespace="profile")),
]
