"""A utility script to load test data into the db"""

from django.core.management.base import BaseCommand

from classroom.factories import StudentFactory, SubjectFactory, TeacherFactory
from classroom.models import Student, Subject, Teacher


class Command(BaseCommand):
    """Management command which cleans and populates database with mock data"""

    help = "Loads fake data into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_BAD_REQUEST("Deleting old data..."))
        Teacher.objects.all().delete()
        Student.objects.all().delete()
        Subject.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating new data..."))
        for _ in range(20):
            TeacherFactory()
            SubjectFactory()

        for _ in range(100):
            StudentFactory()

        print(
            f"""
        Teachers: {Teacher.objects.count()}
        Students: {Student.objects.count()}
        Subjects: {Subject.objects.count()}
        """
        )
        self.stdout.write(self.style.SUCCESS("All done! 💖💅🏻💫"))
