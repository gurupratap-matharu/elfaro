from django.core.management.base import BaseCommand

from classroom.factories import TeacherFactory
from classroom.models import Teacher


class Command(BaseCommand):
    help = "Loads fake data into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO("Deleting old data..."))
        Teacher.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating new data..."))
        for _ in range(20):
            TeacherFactory()

        self.stdout.write(self.style.SUCCESS("All done! 💖"))
