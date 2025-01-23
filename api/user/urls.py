from django.urls import path

from api.user.views import UserView, UserDetailView


app_name = "user"

urlpatterns = [
    path("", UserView.as_view(), name="index"),
    path("<str:id>", UserDetailView.as_view(), name="detail")
]
