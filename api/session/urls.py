from django.urls import path

from api.session.views import SessionView


app_name = "session"

urlpatterns = [
    path("", SessionView.as_view(), name="index"),
]
