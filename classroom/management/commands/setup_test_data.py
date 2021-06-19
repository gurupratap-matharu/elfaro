"""A utility script to load test data into the db"""

import random

import factory
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

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "-l", "--locale", type=str, help="Define a locale for the data to be generated."
        )

    def handle(self, *args, **kwargs):
        locale = kwargs.get("locale")
        self.stdout.write(self.style.SUCCESS("Locale: %s" % locale))

        self.stdout.write(self.style.HTTP_BAD_REQUEST("Deleting old data..."))
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        Subject.objects.all().delete()
        Course.objects.all().delete()
        SubjectGroup.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating new data..."))

        with factory.Faker.override_default_locale(locale):
            teachers = TeacherFactory.create_batch(size=20)
            students = StudentFactory.create_batch(size=100)
            subject_groups = SubjectGroupFactory.create_batch(size=5)

            for _ in range(20):
                SubjectFactory(groups=random.choices(subject_groups, k=3))
                CourseFactory(
                    students=random.choices(students, k=10),
                    teachers=random.choices(teachers, k=3),
                    subject_group=random.choice(subject_groups),
                )

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
