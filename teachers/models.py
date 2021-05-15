import uuid

from django.core.validators import RegexValidator
from django.db import models


class Teacher(models.Model):
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
    ]

    SINGLE = "S"
    MARRIED = "M"
    DIVORCED = "D"
    WIDOWED = "W"
    MARITAL_STATUS = [
        (SINGLE, "Single"),
        (MARRIED, "Married"),
        (DIVORCED, "Divorced"),
        (WIDOWED, "Widowed"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(verbose_name="First name", max_length=200)
    last_name = models.CharField(verbose_name="Last name", max_length=200)
    dni = models.PositiveIntegerField(verbose_name="DNI")
    date_of_birth = models.DateField(verbose_name="Date of birth")
    date_of_admission = models.DateField(verbose_name="Date of admission")
    email = models.EmailField()
    address1 = models.CharField(verbose_name="Address line 1", max_length=200)
    address2 = models.CharField(verbose_name="Address line 2", max_length=200)
    city = models.CharField(verbose_name="City", max_length=60)
    gender = models.CharField(
        verbose_name="Gender", max_length=2, choices=GENDER_CHOICES, default=FEMALE
    )
    marital_status = models.CharField(
        verbose_name="Marital Status", max_length=2, default=SINGLE
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+5491123456789'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    certified = models.BooleanField(default=False)
