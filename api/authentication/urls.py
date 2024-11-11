from django.urls import path

from api.authentication.views import (CreateUserView,
                                      LoginView,
                                      RefreshTokenView,
                                      VerifyOTPView)


app_name = "authentication"

urlpatterns = [
    path("create-user", CreateUserView.as_view(), name="create-user"),
    path("login", LoginView.as_view(), name="login"),
    path("refresh-token", RefreshTokenView.as_view(), name="refresh-token"),
    path("verify-otp", VerifyOTPView.as_view(), name="verify-otp"),
]
