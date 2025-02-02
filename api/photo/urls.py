from django.urls import path

from api.photo.views import PhotoView


app_name = "photo"

urlpatterns = [
    path("<str:session_id>", PhotoView.as_view(), name="index"),
]
