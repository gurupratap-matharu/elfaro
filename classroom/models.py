"""Database models for the elfaro platform"""
import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Person(models.Model):
    """Abstract class which represents a person with common fields"""

    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

    GENDER_CHOICES = [
        (MALE, _("Male")),
        (FEMALE, _("Female")),
        (OTHER, _("Other")),
    ]

    SINGLE = "S"
    MARRIED = "M"
    DIVORCED = "D"
    WIDOWED = "W"

    MARITAL_STATUS_CHOICES = [
        (SINGLE, _("Single")),
        (MARRIED, _("Married")),
        (DIVORCED, _("Divorced")),
        (WIDOWED, _("Widowed")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(verbose_name=_("First name"), max_length=200)
    last_name = models.CharField(verbose_name=_("Last name"), max_length=200)
    dni = models.PositiveIntegerField(
        verbose_name=_("DNI"),
        help_text=_("Your identification number"),
    )
    date_of_birth = models.DateField(
        verbose_name=_("Date of birth"),
        help_text=_("Your date of birth as it appears on your national document"),
    )
    date_of_admission = models.DateField(
        verbose_name=_("Date of admission"),
        help_text=_("The date you registered with us."),
    )
    email = models.EmailField(
        verbose_name=_("Your work email"),
        help_text=_("We will send notification emails to this email address."),
    )
    address1 = models.CharField(verbose_name=_("Address line 1"), max_length=200)
    address2 = models.CharField(verbose_name=_("Address line 2"), max_length=200)
    city = models.CharField(verbose_name=_("City"), max_length=60)
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=2,
        choices=GENDER_CHOICES,
        default=FEMALE,
    )
    marital_status = models.CharField(
        verbose_name=_("Marital Status"),
        max_length=2,
        choices=MARITAL_STATUS_CHOICES,
        default=SINGLE,
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_(
            "Phone number must be entered in the format: '+5491123456789'. "
            "Up to 15 digits allowed. No spaces"
        ),
    )
    phone_number = models.CharField(
        verbose_name=_("Your cellphone number."),
        help_text=_("We might drop you a message incase of an emergency"),
        validators=[phone_regex],
        max_length=17,
        blank=True,
    )

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Teacher(Person):
    """Teacher model which inherits from the Person abstract model."""

    certified = models.BooleanField(
        verbose_name=_("Certified"),
        help_text=_("Are you certified as a teacher?"),
        default=False,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher"
    )

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        ordering = ("-updated",)

    def __str__(self) -> str:
        return ", ".join([self.first_name, self.last_name, str(self.dni)])


class Student(Person):
    """Student model which inherits from the abstract Person model."""

    permission_for_photo = models.BooleanField(
        verbose_name=_("Grant permission for photograph."),
        help_text=_("Whether you give us consent to use your photograph."),
        default=False,
    )
    father_first_name = models.CharField(
        verbose_name=_("Father's First name"), max_length=200, blank=True
    )
    father_last_name = models.CharField(
        verbose_name=_("Father's Last name"), max_length=200, blank=True
    )
    father_dni = models.PositiveIntegerField(
        verbose_name=_("Father's DNI"),
        help_text=_("The national document identification numberr of the applicant's father"),
        null=True,
    )
    father_email = models.EmailField(
        verbose_name=_("Father's email"),
        help_text=_(
            "We might send email to this address for permissions or information regarding the student's activities"
        ),
        blank=True,
    )

    mother_first_name = models.CharField(
        verbose_name=_("Mother First name"), max_length=200, blank=True
    )
    mother_last_name = models.CharField(
        verbose_name=_("Mother Last name"), max_length=200, blank=True
    )
    mother_dni = models.PositiveIntegerField(
        verbose_name=_("Mother's DNI"),
        help_text=_("The national document identification number of the applicant's mother"),
        null=True,
    )
    mother_email = models.EmailField(
        verbose_name=_("Mother's email"),
        help_text=_(
            "We might send email to this address for permissions or information regarding the student's activities"
        ),
        blank=True,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student"
    )

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ("-updated",)

    def __str__(self) -> str:
        return ", ".join([self.first_name, self.last_name, str(self.dni)])


class SubjectGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        verbose_name=_("Subject Group"),
        help_text=_("The group to which the subject belongs."),
        max_length=255,
    )

    year = models.PositiveSmallIntegerField(
        verbose_name=_("Year"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("SubjectGroup")
        verbose_name_plural = _("SubjectGroups")
        ordering = ("-updated",)

    def __str__(self) -> str:
        return ", ".join([self.name, str(self.year)])


class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        verbose_name=_("Subject name"), help_text=_("The name of the subject"), max_length=255
    )
    groups = models.ManyToManyField(SubjectGroup)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ("-updated",)

    def __str__(self) -> str:
        return f"{self.name}"


class Course(models.Model):
    MORNING = "M"
    AFTERNOON = "A"
    EVENING = "E"

    BATCH_CHOICES = (
        (MORNING, _("Morning")),
        (AFTERNOON, _("Afternoon")),
        (EVENING, _("Evening")),
    )

    AULA1 = "A1"
    AULA2 = "A2"
    AULA3 = "A3"
    AULA4 = "A4"
    AULA5 = "A5"
    AULA6 = "A6"
    AULA7 = "A7"
    AULA8 = "A8"
    AULA9 = "A9"
    AULA10 = "A10"
    BIBLIOTECA = "B"
    PATIO = "P"
    CAMPOLTER = "C"
    LABORATORIOFQ = "LF"
    LABORATORIOTECH = "LT"
    LABORATORIOINF = "LI"

    CLASSROOM_CHOICES = (
        (AULA1, "Aula-1"),
        (AULA2, "Aula-2"),
        (AULA3, "Aula-3"),
        (AULA4, "Aula-4"),
        (AULA5, "Aula-5"),
        (AULA6, "Aula-6"),
        (AULA7, "Aula-7"),
        (AULA8, "Aula-8"),
        (AULA9, "Aula-9"),
        (AULA10, "Aula-10"),
        (BIBLIOTECA, "Biblioteca"),
        (PATIO, "Patio"),
        (CAMPOLTER, "Campolter"),
        (LABORATORIOFQ, "Laboratorio FQ"),
        (LABORATORIOTECH, "Laboratorio TECH"),
        (LABORATORIOINF, "Laboratorio De Informatica"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Course Name"), max_length=60)
    batch = models.CharField(
        verbose_name=_("Batch"),
        help_text=_("Time of the day when the course is conducted"),
        max_length=1,
        choices=BATCH_CHOICES,
        default=MORNING,
    )
    classroom = models.CharField(
        verbose_name=_("Classroom"),
        help_text=_("Physical location where the course will be conducted."),
        max_length=3,
        choices=CLASSROOM_CHOICES,
        default=AULA1,
    )
    division = models.PositiveSmallIntegerField(
        verbose_name=_("Division"),
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
    )
    students = models.ManyToManyField(Student)
    teachers = models.ManyToManyField(Teacher)
    subject = models.ForeignKey(
        Subject, on_delete=models.DO_NOTHING, related_name="Course", null=True
    )

    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ("-updated",)

    def __str__(self) -> str:
        return f"{self.name}, {self.batch}, {self.classroom}"

    def get_absolute_url(self):
        return reverse("classroom:course_detail", args=[str(self.id)])
