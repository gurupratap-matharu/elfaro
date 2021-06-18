import factory
from django.utils import timezone
from faker import Faker

from .models import Course, Student, Subject, SubjectGroup, Teacher

fake = Faker()


GENDER_CHOICES = [x[0] for x in Teacher.GENDER_CHOICES]
MARITAL_STATUS_CHOICES = [x[0] for x in Teacher.MARITAL_STATUS_CHOICES]


class TeacherFactory(factory.django.DjangoModelFactory):

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    dni = factory.Faker("random_int", min=10000000, max=99999999)
    date_of_birth = factory.Faker(
        "date_of_birth",
        tzinfo=timezone.get_current_timezone(),
        minimum_age=15,
        maximum_age=40,
    )
    date_of_admission = factory.Faker("date_this_decade")
    email = factory.LazyAttribute(
        lambda obj: "%s@example.com" % (obj.first_name.lower() + obj.last_name.lower())
    )
    address1 = factory.Faker("address")
    address2 = factory.Faker("address")
    city = factory.Faker("city")
    gender = factory.Faker("random_element", elements=GENDER_CHOICES)
    marital_status = factory.Faker("random_element", elements=MARITAL_STATUS_CHOICES)
    phone_number = factory.LazyAttribute(lambda o: "+54911%s" % o.phone_num)
    certified = factory.Faker("boolean")
    active = factory.Faker("boolean")

    class Meta:
        model = Teacher

    class Params:
        phone_num = factory.Faker("randomize_nb_elements", number=50254191)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student


class CourseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Course


class SubjectFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subject


class SubjectGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SubjectGroup
