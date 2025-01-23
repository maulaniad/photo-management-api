from django.urls import path

from api.profile.views import ProfileView, ProfileAvatarView


app_name = "profile"

urlpatterns = [
    path("", ProfileView.as_view(), name="index"),
    path("avatar", ProfileAvatarView.as_view(), name="avatar"),
]
