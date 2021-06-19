"""A utility script to load test data into the db"""

import random

from django.core.management.base import BaseCommand

from classroom.factories import (
    CourseFactory,
    StudentFactory,
    SubjectFactory,
    SubjectGroupFactory,
    TeacherFactory,
)
from classroom.models import Course, Student, Subject, SubjectGroup, Teacher


class Command(BaseCommand):
    """Management command which cleans and populates database with mock data"""

    help = "Loads fake data into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_BAD_REQUEST("Deleting old data..."))
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        SubjectGroup.objects.all().delete()
        Subject.objects.all().delete()
        Course.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating new data..."))

        for _ in range(5):
            SubjectGroupFactory()

        subject_groups = SubjectGroup.objects.all()

        for _ in range(20):
            TeacherFactory()

            groups = random.choices(subject_groups, k=3)
            SubjectFactory(groups=groups)

        for _ in range(100):
            StudentFactory()

        for _ in range(20):
            CourseFactory()

        print(
            f"""
        Teachers: {Teacher.objects.count()}
        Students: {Student.objects.count()}
        Subjects: {Subject.objects.count()}
        Subject Groups: {SubjectGroup.objects.count()}
        Courses: {Course.objects.count()}
        """
        )
        self.stdout.write(self.style.SUCCESS("All done! 💖💅🏻💫"))
