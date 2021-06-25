from django.urls import path

from .views import CourseDetailView, CourseListView, HomePageView

app_name = "classroom"

urlpatterns = [
    path("", HomePageView.as_view(), name="classroom_home"),
    path("courses/", CourseListView.as_view(), name="course_list"),
    path("courses/<uuid:pk>/", CourseDetailView.as_view(), name="course_detail"),
]
