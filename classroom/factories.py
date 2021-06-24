"""
Factories for all the models of the classroom app. They heavily use factory-boy
and the excellent faker module under the hood to generate authentic fake data.

Meant to be used in 
    - unit tests
    - management commands
"""

import factory
from django.utils import timezone

from users.factories import UserFactory

from .models import Course, Student, Subject, SubjectGroup, Teacher

LOCALE = "es"

GENDER_CHOICES = [x[0] for x in Teacher.GENDER_CHOICES]
MARITAL_STATUS_CHOICES = [x[0] for x in Teacher.MARITAL_STATUS_CHOICES]
BATCH_CHOICES = [x[0] for x in Course.BATCH_CHOICES]
CLASSROOM_CHOICES = [x[0] for x in Course.CLASSROOM_CHOICES]


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
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Teacher

    class Params:
        phone_num = factory.Faker("randomize_nb_elements", number=50254191)


class StudentFactory(factory.django.DjangoModelFactory):
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
    permission_for_photo = factory.Faker("boolean")
    father_first_name = factory.Faker("first_name_male")
    father_last_name = factory.Faker("last_name_male")
    father_dni = factory.Faker("random_int", min=10000000, max=99999999)
    father_email = factory.LazyAttribute(
        lambda obj: "%s@example.com"
        % (obj.father_first_name.lower() + obj.father_last_name.lower())
    )
    mother_first_name = factory.Faker("first_name_female")
    mother_last_name = factory.Faker("last_name_female")
    mother_dni = factory.Faker("random_int", min=10000000, max=99999999)
    mother_email = factory.LazyAttribute(
        lambda obj: "%s@example.com"
        % (obj.mother_first_name.lower() + obj.mother_last_name.lower())
    )
    active = factory.Faker("boolean")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Student

    class Params:
        phone_num = factory.Faker("randomize_nb_elements", number=50254191)


class SubjectFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("catch_phrase")
    active = factory.Faker("boolean")

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """
        A factory-boy hook that adds a subject to respective groups after creation
        The groups have to be explicitly passed upon creation.

        Ex:
        SubjectFactory() # will not add to any groups
        SubjectFactory(groups=(group1, group2)) # will add to mentioned groups
        """

        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)

    class Meta:
        model = Subject


class SubjectGroupFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "Group #%s" % n)
    year = factory.Faker("random_int", min=1, max=6)
    active = factory.Faker("boolean")

    class Meta:
        model = SubjectGroup


class CourseFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("color_name")
    batch = factory.Faker("random_element", elements=BATCH_CHOICES)
    classroom = factory.Faker("random_element", elements=CLASSROOM_CHOICES)
    division = factory.Faker("random_int", min=1, max=6)
    subject_group = factory.SubFactory(SubjectGroupFactory)
    active = factory.Faker("boolean")

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        """
        A factory-boy hook that adds students to a course after creation
        The students have to be explicitly passed upon creation.

        Ex:
        CourseFactory() # will not add to any students
        CourseFactory(students=(student1, student2)) # will add those students
        """

        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of students were passed in, use them
            for student in extracted:
                self.students.add(student)

    @factory.post_generation
    def teachers(self, create, extracted, **kwargs):
        """
        A factory-boy hook that adds teachers to a course after creation
        The teachers have to be explicitly passed upon creation.

        Ex:
        CourseFactory() # will not add to any teachers
        CourseFactory(teachers=(teacher1, teacher2)) # will add those teachers
        """

        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of students were passed in, use them
            for teacher in extracted:
                self.teachers.add(teacher)

    class Meta:
        model = Course
