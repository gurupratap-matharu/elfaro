"""Views for the ElFaro app"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView

from classroom.models import Course


class HomePageView(TemplateView):
    """A simple template view to show the default homepage"""

    template_name = "classroom/home.html"


class CourseListView(LoginRequiredMixin, ListView):
    """Lists all the courses for a particular teacher"""

    model = Course
    context_object_name = "course_list"
    template_name = "classroom/course_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(teachers=self.request.user.teacher)

        return queryset


class CourseDetailView(LoginRequiredMixin, DetailView):
    """Renders a detailed view for a course"""

    model = Course
    context_object_name = "course"
    template_name = "classroom/course_detail.html"
