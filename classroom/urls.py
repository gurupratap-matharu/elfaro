from django.urls import path

from .views import HomePageView

app_name = "classroom"

urlpatterns = [
    path("", HomePageView.as_view(), name="classroom_home"),
]
